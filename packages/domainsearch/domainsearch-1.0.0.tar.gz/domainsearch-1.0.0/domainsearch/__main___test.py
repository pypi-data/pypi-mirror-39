from .__main__ import Wildcard, Whois, consonants, vowels, numbers, main
import itertools
import pytest


def test_wildcard():
    assert tuple(Wildcard('test').values) == ('test',)
    assert tuple(Wildcard('t?').values) == ('', 't')
    assert tuple(Wildcard('testCV#').values) == tuple(
        'test' + ''.join(match)
        for match in itertools.product(consonants, vowels, numbers))


def test_main_help(capsys):
    with pytest.raises(SystemExit):
        main(['domainsearch', '-h'])
    captured = capsys.readouterr()
    assert 'usage: domainsearch' in captured.out


def test_main_lookup(capsys):
    main(['domainsearch', 'test[ab].com'])
    captured = capsys.readouterr()
    assert 'testa.com' in captured.out
    assert 'testb.com' in captured.out
