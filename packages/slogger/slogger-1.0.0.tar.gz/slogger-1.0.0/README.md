# slogger

slogger is designed as simple a logger for configuration in your python program. The is based on the python `logging` module, but it is more simple to configure.

## Installation
`pip install slogger`

## API
### Get logger instance
```
from slogger import Logger

logger = Logger.getLogger(__name__)

```
`Logger.getLogger(__name__)` returns a logger with category. 

### Work with logger
```
logger.debug(obj)
logger.info(obj)
logger.warning(obj)
logger.error(obj)
logger.critical(obj)
```
The above functions work similar as those in native logging functions. The different is that all of them return the `obj` parameter again.

```
obj1 = logger.debug(obj)

print(obj1 == obj) # True

```

### Work with logger and title
```
logger.title("title").debug(obj)
logger.title("title").info(obj)
logger.title("title").warning(obj)
logger.title("title").error(obj)
logger.title("title").critical(obj)
```
The above functions behave exactly the same as the native functions except that a title is added.
```
name = "alan"
logger.title("name").debug(name) # output: name--alan
```
It is useful when you want to give a simple descirption of your logging data.


## Configuration
### Configuration for std output
Do nothing except for `logging.basicConfig(level=logging.DEBUG)` to use the logger. It is useful when you run your unit test and want to see the log information on the screen.

### Configuration for file output
Add the file `slogger.cfg` at the root of execution folder. The configuration schema is as following.
```
[handlers]
<filename_level>:[!],[<category>],[<category...>]
```
**filename**: the name of the file to hold the output of the log. Currently, it is default as `TimedRotatingFileHandler`.   

**level**: the level for logging. It should be one of following value
- all
- notset
- debug
- info
- warning
- error
- critical

**category**: the name of category to filter out the log. Examples:
- `app_all: app` means only the log information with category name `app` can be output to the log file `app.log` at the root of execution folder. 
- `others_all:!, app` means all the log information except with category name `app` can be output to the log file `other.log` at the root of execution folder.

