

class ReplaceException(Exception):

	def __init__(self, pattern, replacement):
		self.pattern = pattern
		self.replacement = replacement
		super().__init__("Replace: " + repr(pattern) + " with " + repr(replacement))
	#

#


