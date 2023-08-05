#!/usr/bin/env python3
from functools import reduce
from .version import __version__
import argparse
import itertools
import socket
import sys


HOST = 'whois.crsnic.net'
PORT = 43


class Whois:
    def __init__(self, server, port):
        self.server = server
        self.port = port

    def lookup(self, domain, verbose=False):
        """Looks up the domain. Returns true if domain is registered,
        false otherwise"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server, self.port))
        sock.send(("%s\r\n" % domain).encode("utf-8"))

        try:
            value = self._recv(sock)
        finally:
            # sock.shutdown(socket.SHUT_RDWR)
            sock.close()

        if verbose:
            print(value)

        if 'No match for nameserver' in value:
            return None
        if 'No match for' in value:
            return False
        return True

    def _recv(self, sock):
        buff = b""
        while True:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            buff += data
        return buff.decode("utf-8")


alphabet = tuple('abcdefghijklmnopqrstuvwxyz')
numbers = tuple('0123456789')
alphanumeric = alphabet + numbers
vowels = tuple('aeiou')
consonants = tuple(c for c in alphabet if c not in set(vowels))


class Wildcard:
    def __init__(self, wildcard):
        self.wildcard = wildcard

        self.wildcards = wildcards = []
        self.letters = letters = []

        bracket_open = False
        parenthesis_open = False
        tmp = None
        tmp_list = None
        for i, c in enumerate(self.wildcard):
            if c == '[':
                self._assert(
                    not bracket_open and not parenthesis_open,
                    'Wildcard compile error at: {}'.format(i))
                bracket_open = True
                tmp = ''
            elif c == ']':
                self._assert(
                    bracket_open,
                    'Closing brace: {}'.format(i))
                bracket_open = False
                wildcards.append(tuple(tmp))
                tmp = None
                letters.append('_')
            elif bracket_open:
                tmp += c
            elif c == '(':
                self._assert(
                    not bracket_open and not parenthesis_open,
                    'Wildcard compile error at: {}'.format(i))
                parenthesis_open = True
                tmp_list = ['']
            elif c == ')':
                self._assert(
                    parenthesis_open,
                    'Closing parenthesis: {}'.format(i))
                wildcards.append(tuple(tmp_list))
                letters.append('_')
                parenthesis_open = False
            elif c == ',' and parenthesis_open:
                tmp_list.append('')
            elif parenthesis_open:
                tmp_list[-1] += c
            elif c == 'A':
                wildcards.append(alphabet)
                letters.append('_')
            elif c == 'C':
                wildcards.append(consonants)
                letters.append('_')
            elif c == 'V':
                wildcards.append(vowels)
                letters.append('_')
            elif c == '*':
                wildcards.append(alphanumeric)
                letters.append('_')
            elif c == '#':
                wildcards.append(numbers)
                letters.append('_')
            elif c == '?':
                self._assert(i > 0, 'Cannot use ? as the first character')
                if wildcards and '' in wildcards[-1]:
                    continue
                last_letter = letters[-1]
                if last_letter == '_':
                    wildcards[-1] = ('',) + wildcards[-1]
                else:
                    wildcards.append(('', last_letter))
                    letters[-1] = '_'
            else:
                letters.append(c)

        if bracket_open:
            raise ValueError('Wildcard compile error: no closing bracket')
        if parenthesis_open:
            raise ValueError('Wildcard compile error: no closing parenthesis')
        self.combinations = reduce(lambda x, y: x * len(y), wildcards, 1)

    def _assert(self, value, message):
        if not value:
            raise ValueError(message)

    @property
    def values(self):
        wildcards = self.wildcards
        letters = self.letters

        if len(wildcards) == 0:
            yield self.wildcard
            return

        product = itertools.product(*wildcards)

        for p in product:
            word = ''
            i = -1
            for ll in letters:
                if ll == '_':
                    i += 1
                    word += p[i]
                else:
                    word += ll
            yield word


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog='domainsearch',
        description='Search for unregistered domains. Wildcards supported are:'
        '\n  A: alphabet characters'
        '\n  C: consonants'
        '\n  V: vowels'
        '\n  #: numbers 0-9'
        '\n  *: combination of all of the above'
        '\n  [chars]: chars in the brackets'
        '\n  (word1,word2,word3): custom list of words',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--host', default=HOST,
                        help='of the Whois lookup server')
    parser.add_argument('--port', default=PORT, type=int,
                        help='Port of the Whois lookup server')
    parser.add_argument('-n', '--dry-run', default=False, action='store_true',
                        help='Only print the permutations')
    parser.add_argument('-o', '--only', default=False, action='store_true',
                        help='Print only available')
    parser.add_argument('--verbose', default=False, action='store_true',
                        help='Show whois results')
    parser.add_argument('-v', '--version', default=False, action='store_true',
                        help='Print version information and exit')
    parser.add_argument('domains', nargs='*',
                        help='Domain(s) to look up. For example redCV.com')

    return parser.parse_args(argv)


class Logger:
    def __init__(self):
        self.stderr_width = 0

    def progress(self, string, *values):
        value = string.format(*values) + '\r'
        sys.stderr.write(value)
        sys.stderr.flush()
        self.stderr_width = len(value) - 1

    def log(self, message, *values):
        value = message.format(*values)
        spaces = max(0, self.stderr_width - len(value))
        print('{}{}'.format(value, ' ' * spaces))
        self.stderr_width = 0


def main(argv=sys.argv[1:]):
    args = parse_args(argv)

    host = args.host
    port = args.port

    logger = Logger()

    if args.version:
        logger.log('domainsearch v{}', __version__)
        return

    whois = Whois(host, port)

    domains = args.domains
    total = 0
    total_avail = 0
    for domain in domains:
        if '.' not in domain:
            domain += '.com'

        wildcard = Wildcard(domain)
        combinations = wildcard.combinations

        for i, domain in enumerate(wildcard.values):
            count = i + 1
            # if count % 10 == 0:
            logger.progress('  {} ({} of {})', domain, count, combinations)

            if args.dry_run:
                logger.log(domain)
                continue

            registered = whois.lookup(domain, verbose=args.verbose)
            total += 1
            if registered is None:
                logger.log('  {} (invalid request)', domain)
            elif not registered:
                total_avail += 1
                logger.log('✓ {}', domain)
            elif not args.only:
                logger.log('✕ {}', domain)

    logger.progress('{} available domains of {}\n', total_avail, total)


def init(name, argv=sys.argv[1:]):
    if name == '__main__':
        main(argv)
