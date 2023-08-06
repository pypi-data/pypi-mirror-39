""" Settings submodule """

# Forward or reverse modes, options are "reverse" or "forward"
__DEFAULT_AD_MODE__ = "forward"

class Settings():
	def __init__(self):
		self.mode = __DEFAULT_AD_MODE__

	def set_mode(self, mode):
		if mode not in ["reverse", "forward"]:
			raise ValueError("Mode must be either \"forward\" or \"reverse\"")
		self.mode = mode

	def current_mode(self):
		return self.mode

# Global settings
settings = Settings()
