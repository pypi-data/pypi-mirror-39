

class ReplaceException(Exception):

	def __init__(self, nItemPos, pattern, replacement):
		self.nItemPos = nItemPos
		self.pattern = pattern
		self.replacement = replacement
		super().__init__("Replace: " + repr(pattern) + " with " + repr(replacement))
	#

#


