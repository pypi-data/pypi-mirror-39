from colorama import Fore, Style, init
import colorama

colorama.init(strip=False)
init()


class btext:

    def __init__(self):
        print(Style.RESET_ALL)

    @staticmethod
    def success(string):
        print(Fore.GREEN + '[SUCCESS] ' + str(string) + Style.RESET_ALL)

    @staticmethod
    def info(string):
        print(Fore.YELLOW + '[INFO] ' + str(string) + Style.RESET_ALL)

    @staticmethod
    def warning(string):
        print(Fore.RED + '[WARNING] ' + str(string) + Style.RESET_ALL)

    @staticmethod
    def error(string):
        print(Fore.LIGHTRED_EX + '[ERROR] ' + str(string) + Style.RESET_ALL)

    @staticmethod
    def debug(string):
        print(Fore.MAGENTA + '[DEBUG] ' + str(string) + Style.RESET_ALL)

    @staticmethod
    def custom(string1, string2):
        print(Fore.CYAN + '[%s] ' % str(string1) + str(string2) + Style.RESET_ALL)

    @staticmethod
    def demo():
        btext.success("your string")
        btext.info("your string")
        btext.warning("your string")
        btext.error("your string")
        btext.debug("your string")
        btext.custom("your prefix", "your string")
