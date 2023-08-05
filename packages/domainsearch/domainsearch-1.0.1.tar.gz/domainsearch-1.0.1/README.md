# domainsearch

[![Build Status](https://travis-ci.com/jeremija/domainsearch.svg?branch=master)](https://travis-ci.com/jeremija/domainsearch)

Search for available domains using wildcards.

# Install

```
git clone https://github.com/jeremija/domainsearch
cd domainsearch
python3 -m domainsearch
```

or

```
pip3 install domainsearch
```

# Usage

```bash
usage: domainsearch [-h] [--host HOST] [--port PORT] [-n] [-o] [--verbose]
                    domains [domains ...]

Search for unregistered domains. Wildcards supported are:
  A: alphabet characters
  C: consonants
  V: vowels
  #: numbers 0-9
  *: combination of all of the above
  [chars]: chars in the brackets
  (word1,word2,word3): custom list of words

positional arguments:
  domains        Domain(s) to look up. For example redCV.com

optional arguments:
  -h, --help     show this help message and exit
  --host HOST    of the Whois lookup server
  --port PORT    Port of the Whois lookup server
  -n, --dry-run  Only print the permutations
  -o, --only     Print only available
  --verbose      Show whois results
```

# License

MIT
