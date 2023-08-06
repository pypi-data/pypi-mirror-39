

import time
import threading
import contextlib
import re

import treetaggerwrapper as ttpw

from .ObservableEvent import ObservableEvent
from .ReplaceException import ReplaceException



#
# This class wraps around tree taggers. It is best suitable for use in concurrent, multithreaded environments.
#
class PoolOfThreadedTreeTaggers(object):

	_SPLIT_PATTERN = re.compile("^([^\t]+)\t(.+)\s+(.+)\s+([^\s]+)$")
	_SPLIT_PATTERN_2 = re.compile("^<([^\s]+)\s+text=\"(.+)\"\s*/>$")

	class _LangSpecificCache(object):

		def __init__(self, langID:str):
			self.langID = langID
			self.idleInstances = []
			self.lastAccess = time.time()
			self.countUsedInstances = 0
			self.langLock = threading.Lock()
		#

		def touch(self):
			self.lastAccess = time.time()
		#
	#

	################################################################
	#### Constructors / Destructors
	################################################################

	def __init__(self, treeTaggerInstallationPath:str):
		self.__treeTaggerInstallationPath = treeTaggerInstallationPath
		self.__unused = {}
		self.__onTaggerCreated = ObservableEvent("onTaggerCreated")

		self.__mainLock = threading.Lock()
	#

	################################################################
	#### Events
	################################################################

	#
	# This property returns an event object. Whenever a new TreeTagger process is created, this event is fired.
	#
	@property
	def onTaggerCreated(self):
		return self.__onTaggerCreated
	#

	################################################################
	#### Methods
	################################################################

	#
	# This method must be used together with the "with" statement to retrieve and use a <c>treetaggerwrapper</c> object.
	#
	# Have a look at <c>tagText()</c>: That method might be exactly what you are looking for as <c>tagText()</c> is implemented as this:
	#
	# <code>
	#	def tagText(self, langID:str, text:str) -> str:
	#		with self._useTagger(langID) as tagger:
	#			return tagger.tag_text(text)
	# </code>
	#
	@contextlib.contextmanager
	def _useTagger(self, langID:str):
		assert isinstance(langID, str)

		with self.__mainLock:
			langIDCache = self.__unused.get(langID, None)
			if langIDCache is None:
				langIDCache = PoolOfThreadedTreeTaggers._LangSpecificCache(langID)
				self.__unused[langID] = langIDCache

		langIDCache.touch()

		if langIDCache.idleInstances:
			with langIDCache.langLock:
				tagger = langIDCache.idleInstances[-1]
				del langIDCache.idleInstances[-1]
				langIDCache.countUsedInstances += 1
		else:
			tagger = ttpw.TreeTagger(
				TAGLANG=langID,
				TAGOPT="-prob -threshold 0.7 -token -lemma -sgml -quiet",
				TAGDIR=self.__treeTaggerInstallationPath)
			self.__onTaggerCreated.fire(self, langID)
			with langIDCache.langLock:
				langIDCache.countUsedInstances += 1

		try:
			yield tagger
		finally:
			with langIDCache.langLock:
				langIDCache.countUsedInstances -= 1
				langIDCache.idleInstances.append(tagger)
	#

	#
	# Convenience method that grabs a free instance of a suitable <c>TreeTagger</c>, tags the data, returns the tree tagger instance used
	# and then returns the tagging result to the caller.
	#
	def tagText(self, langID:str, text:str) -> str:
		assert isinstance(text, str)

		with self._useTagger(langID) as tagger:
			return tagger.tag_text(text)
	#

	def __parseSpecial(self, text, item, gID, gContent, bWithConfidence):
		if gID == "repdns":
			pos = gContent.rfind(".")
			if pos > 0:
				lastPartC = gContent[pos + 1]
				if lastPartC.isupper():
					raise ReplaceException(gContent, gContent[:pos + 1] + " " + gContent[pos:])
				else:
					if bWithConfidence:
						return (
							gContent,
							"§DNS§",
							gContent,
							1,
						)
					else:
						return (
							gContent,
							"§DNS§",
							gContent,
						)
		elif gID == "repemail":
			if bWithConfidence:
				return (
					gContent,
					"§EMAIL§",
					gContent,
					1,
				)
			else:
				return (
					gContent,
					"§EMAIL§",
					gContent,
				)
		elif gID == "repurl":
			if bWithConfidence:
				return (
					gContent,
					"§URL§",
					gContent,
					1,
				)
			else:
				return (
					gContent,
					"§URL§",
					gContent,
				)
		else:
			print()
			print(text)
			print("No suitable pattern: " + item)
			print()
			if bWithConfidence:
				return (
					None,
					None,
					None,
					None,
				)
			else:
				return (
					None,
					None,
					None,
				)

	#

	#
	# Convenience method that grabs a free instance of a suitable <c>TreeTagger</c>, tags the data, returns the tree tagger instance used
	# and then returns the tagging result to the caller.
	#
	# @param	bool bWithConfidence		A boolean value indicating wether to add the last confidence value or ignore it in the output
	# @return	list						Returns a list of 3- respectively 4-tuples, where each tuple consists of these entries:
	#										* str : The token tagged (= the input data)
	#										* str : The type of that token (with extra token types: "§EMAIL§", "§URL§")
	#										* str : The lemma as a string or <c>None</c> if tagging failed
	#										* float : The confidence value
	#
	def tagText2(self, langID:str, text:str, bWithConfidence:bool = True, bWithNullsInsteadOfUnknown:bool = True) -> list:
		assert isinstance(bWithConfidence, bool)
		assert isinstance(bWithNullsInsteadOfUnknown, bool)
		if not bWithNullsInsteadOfUnknown:
			raise NotImplementedError("bWithNullsInsteadOfUnknown = False")
		assert isinstance(langID, str)
		assert isinstance(text, str)

		n = 100
		while True:
			try:
				n -= 1
				return self.__tagText2(langID, text, bWithConfidence, bWithNullsInsteadOfUnknown)
			except ReplaceException as ee:
				if n == 0:
					raise Exception("Endless loop! " + repr(text))
				text = text.replace(ee.pattern, ee.replacement, 1)
	#

	def __tagText2(self, langID:str, text:str, bWithConfidence:bool = True, bWithNullsInsteadOfUnknown:bool = True) -> list:
		if bWithConfidence:
			with self._useTagger(langID) as tagger:
				ret = []
				for item in tagger.tag_text(text):
					result = PoolOfThreadedTreeTaggers._SPLIT_PATTERN_2.match(item)
					if result != None:
						special = self.__parseSpecial(
							text,
							item,
							result.group(1),
							result.group(2),
							bWithConfidence
							)
						if special[0] != None:
							del ret[-1]
							ret.append(special)
						else:
							ret.append(special)
					else:
						result = PoolOfThreadedTreeTaggers._SPLIT_PATTERN.match(item)
						if result != None:
							g3 = result.group(3)
							if bWithNullsInsteadOfUnknown:
								ret.append((
									result.group(1),
									result.group(2),
									None if g3 == "<unknown>" else g3,
									float(result.group(4)),
								))
							else:
								ret.append((
									result.group(1),
									result.group(2),
									g3,
									float(result.group(4)),
								))
						else:
							print()
							print(text)
							print("No suitable pattern: " + item)
							print()
							ret.append((
								None,
								None,
								None,
								None,
							))
				return ret

		else:
			with self._useTagger(langID) as tagger:
				ret = []
				for item in tagger.tag_text(text):
					result = PoolOfThreadedTreeTaggers._SPLIT_PATTERN_2.match(item)
					if result != None:
						special = self.__parseSpecial(
							text,
							item,
							result.group(1),
							result.group(2),
							bWithConfidence
							)
						if special[0] != None:
							del ret[-1]
							ret.append(special)
						else:
							ret.append(special)
					else:
						result = PoolOfThreadedTreeTaggers._SPLIT_PATTERN.match(item)
						if result != None:
							g3 = result.group(3)
							if bWithNullsInsteadOfUnknown:
								ret.append((
									result.group(1),
									result.group(2),
									None if g3 == "<unknown>" else g3,
								))
							else:
								ret.append((
									result.group(1),
									result.group(2),
									g3,
								))
						else:
							print()
							print(text)
							print("No suitable pattern: " + item)
							print()
							ret.append((
								None,
								None,
								None,
								None,
							))
				return ret
	#

	#
	# Retrieve statistical information about the tagging instances maintained in the background.
	#
	def getStats(self):
		with self.__mainLock:
			allTuples = list(self.__unused.items())

		ret = {}
		for langID, langIDCache in allTuples:
			ret[langID] = {
				"idle": len(langIDCache.idleInstances),
				"inUse": langIDCache.countUsedInstances
			}
		return ret
	#

#








