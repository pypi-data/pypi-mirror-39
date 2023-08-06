import logging
import os
import sys
from .util import buildLogContent
from .handler import loadHandlers

class _Logger:
    def __init__(master):
        def getLogger(category):
            class pureLogger:
                def __init__(self, title = None):
                    self.logger = loadHandlers(logging.getLogger(category), category)
                    
                    def debug(obj):
                        self.logger.debug(buildLogContent(title, obj))

                    def info(obj):
                        self.logger.info(buildLogContent(title, obj))

                    def error(obj):
                        self.logger.error(buildLogContent(title, obj))

                    def warning(obj):
                        self.logger.warning(buildLogContent(title, obj))

                    self.debug = debug
                    self.info = info
                    self.error = error
                    self.warning = warning
                    
            class innerLogger:
                def __init__(self):
                    _pureLogger = pureLogger()

                    self.debug = _pureLogger.debug
                    self.info = _pureLogger.info
                    self.error = _pureLogger.error
                    self.warning = _pureLogger.warning

                    def title(title):
                        return pureLogger(title)

                    self.title = title
                    
            return innerLogger()
        
        master.getLogger = getLogger
        
        

Logger = _Logger()

def log(moduleName):
    def title(title = None):
        class GetLogger:
            def __init__(self):

                def has_config_file():
                    return os.path.exists("logger.conf")

                def get_std_logger():
                    return logging.getLogger(moduleName + "--%s" % title if title else "")

                def get_configured_logger():
                    pass
                
                self.logger = get_configured_logger() if has_config_file() else get_std_logger()                
            def debug(self, val):
                self.logger.debug(val)
                return val

            def info(self, val):
                self.logger.info(val)
                return val

            def error(self, val):
                self.logger.error(val)
                return val

        return GetLogger()

    return title
