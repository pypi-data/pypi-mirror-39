"""
CARPI COMMONS
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""


class ExitCodes:
    """
    List of valid exit codes;
    Daemon exceptions create exit codes with value 0xFXXX
    """

    OK = 0x0000
    """ Expected when shutting down """

    UNKNOWN = 0xFFFF
    """ Unknown error, unhandled exception or CarPiExitException without error code """

    CONFIG_FAIL = 0xF000
    """ Failure when loading configuration """


class CarPiExitException(BaseException):
    def __init__(self,
                 exit_code=ExitCodes.UNKNOWN):
        self._exit_code = exit_code

    @property
    def exit_code(self):
        return self._exit_code

    @property
    def exc_message(self):
        return u"An unknown exception has occurred. " \
               "The application code will exit with exit code {}".format(self.exit_code)

    def __str__(self) -> str:
        return self.exc_message


class ConfigFileLoadError(CarPiExitException):
    def __init__(self, requested_log_file: str) -> None:
        CarPiExitException.__init__(self,
                                    exit_code=ExitCodes.CONFIG_FAIL)
        self._requested_log_file = requested_log_file

    @property
    def requested_log_file(self) -> str:
        return self._requested_log_file

    @property
    def exc_message(self):
        return u"Failed to load configuration file {}".format(self.requested_log_file)
