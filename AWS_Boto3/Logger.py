class Logger:
    HEADER = '\033[96m'
    MAGENTA = '\033[95m'
    CYAN = "\033[36m"
    OK_GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    END_C = '\033[0m'
    BOLD = "\033[1m"
    WARNING = "\033[33m"

    @classmethod
    def disable_color(cls):
        cls.HEADER = ''
        cls.MAGENTA = ''
        cls.CYAN = ''
        cls.OK_GREEN = ''
        cls.YELLOW = ''
        cls.FAIL = ''
        cls.END_C = ''
        cls.BOLD = ''
        cls.WARNING = ''

    @classmethod
    def enable_color(cls):
        cls.HEADER = '\033[96m'
        cls.MAGENTA = '\033[95m'
        cls.CYAN = "\033[36m"
        cls.OK_GREEN = '\033[92m'
        cls.YELLOW = '\033[93m'
        cls.FAIL = '\033[91m'
        cls.END_C = '\033[0m'
        cls.BOLD = "\033[1m"
        cls.WARNING = "\033[33m"

    @classmethod
    def info(cls, message):
        print(cls.YELLOW + message + cls.END_C)

    @classmethod
    def header(cls, message):
        print(cls.HEADER + message + cls.END_C)

    @classmethod
    def sub_info(cls, message):
        print(cls.MAGENTA + message + cls.END_C)

    @classmethod
    def avail_info(cls, message):
        print(cls.OK_GREEN + message + cls.END_C)

    @classmethod
    def warn(cls, message):
        print(cls.WARNING + message + cls.END_C)

    @classmethod
    def err(cls, message):
        print(cls.FAIL + str(message) + cls.END_C)
