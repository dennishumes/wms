

class Config(object):
	"""
	configurations that are common across  all environments
	"""

class DevelopmentConfig(Config):
	"""
	dev configs
	"""
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DEBUG = True
	SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
	"""
	Production configs

	"""

	DEBUG = False

app_config = {
	"dev": DevelopmentConfig,
	"prod": ProductionConfig

}