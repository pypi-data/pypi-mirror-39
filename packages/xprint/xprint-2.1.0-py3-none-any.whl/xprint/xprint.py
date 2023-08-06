# coding:utf-8
import sys
import colorama
from colorama import Fore, Back, Style

wr = sys.stdout.write


def init(autoreset: bool = False, convert=None, strip=None, wrap=True):
    colorama.init(autoreset=autoreset, convert=convert, strip=strip, wrap=wrap)


def fi(inline: bool = True):
    if inline:
        wr(Style.RESET_ALL)
    else:
        print(Style.RESET_ALL)
    sys.stdout.flush()


def fx():  # same to fi(inline=False)
    print(Style.RESET_ALL)
    sys.stdout.flush()


def ex():
    print()
    print()
    exit()


def step():
    wr(Fore.LIGHTBLACK_EX + '>')
    fi()


def success(s, inline: bool = False):
    wr(Fore.GREEN + str(s))
    fi(inline)


def error(s, inline: bool = False):
    wr(Back.RED + Fore.LIGHTWHITE_EX + ' {} '.format(s))
    fi(inline)


def value(s, inline: bool = False):
    wr(Fore.LIGHTCYAN_EX + str(s))
    fi(inline)


def job(s):
    print()
    wr(Back.BLUE + Fore.LIGHTWHITE_EX + ' - {} - '.format(s))
    fx()


def about_to(left, value=None, right=None, inline: bool = False):
    wr(Fore.LIGHTBLACK_EX + '> ')
    wr(Fore.LIGHTYELLOW_EX + left)
    if value: wr(Fore.LIGHTCYAN_EX + ' {}'.format(value))
    if right: wr(Fore.LIGHTYELLOW_EX + ' {}'.format(right))
    if inline: wr(Fore.LIGHTBLACK_EX + '... ')
    fi(inline)


def about_t(left, value=None, right=None):
    about_to(left=left, value=value, right=right, inline=True)


def getting(s, inline: bool = True):
    wr(Fore.LIGHTBLACK_EX + '> ')
    wr(Fore.LIGHTYELLOW_EX + str(s))
    wr(Fore.LIGHTBLACK_EX + ' > ')
    fi(inline)


def watching(s, inline: bool = True):
    wr(Fore.LIGHTBLACK_EX + '> ')
    wr(Fore.LIGHTYELLOW_EX + str(s))
    wr(Fore.LIGHTBLACK_EX + ' >')
    fi(inline)
