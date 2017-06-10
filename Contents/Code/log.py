# noinspection PyClassHasNoInit
class LogLevel:
    DEBUG, INFO, WARN, ERROR, CRITICAL, EXCEPTION = range(6)


# noinspection PyClassHasNoInit
class PlexLog:
    log_map = {
        'Debug': LogLevel.DEBUG,
        'Info': LogLevel.INFO,
        'Warn': LogLevel.WARN,
        'Error': LogLevel.ERROR,
        'Critical': LogLevel.CRITICAL,
        'Exception': LogLevel.EXCEPTION
    }

    @staticmethod
    def get_log_level():
        key = Prefs["LogLevel"]
        return PlexLog.log_map.get(key, LogLevel.INFO)

    @staticmethod
    def should_log(level):
        return level >= PlexLog.get_log_level()

    @staticmethod
    def debug(message, *args, **kwargs):
        if PlexLog.should_log(LogLevel.DEBUG):
            Log.Debug(message, *args, **kwargs)

    @staticmethod
    def info(message, *args, **kwargs):
        if PlexLog.should_log(LogLevel.INFO):
            Log.Info(message, *args, **kwargs)

    @staticmethod
    def warn(message, *args, **kwargs):
        if PlexLog.should_log(LogLevel.WARN):
            Log.Warn(message, *args, **kwargs)

    @staticmethod
    def error(message, *args, **kwargs):
        if PlexLog.should_log(LogLevel.ERROR):
            Log.Error(message, *args, **kwargs)

    @staticmethod
    def critical(message, *args, **kwargs):
        if PlexLog.should_log(LogLevel.CRITICAL):
            Log.Critical(message, *args, **kwargs)

    @staticmethod
    def exception(message, *args, **kwargs):
        if PlexLog.should_log(LogLevel.EXCEPTION):
            Log.Exception(message, *args, **kwargs)
