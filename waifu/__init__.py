from termcolor import colored

__VERSIONS__ = "v1.0"

TIT = """
###############################################################################
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗    ██╗ █████╗ ██╗███████╗██╗   ██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║    ██║██╔══██╗██║██╔════╝██║   ██║
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║ █╗ ██║███████║██║█████╗  ██║   ██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║███╗██║██╔══██║██║██╔══╝  ██║   ██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║╚███╔███╔╝██║  ██║██║██║     ╚██████╔╝
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚═╝      ╚═════╝
                                                                {__VERSIONS__}  BY Yuan.
###############################################################################
""".format(__VERSIONS__=__VERSIONS__)

print(colored(TIT, 'green'))