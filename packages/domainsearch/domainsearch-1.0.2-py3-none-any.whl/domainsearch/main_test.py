from .main import \
  Wildcard, \
  alphabet, \
  alphanumeric, \
  consonants, \
  main, \
  numbers, \
  vowels
from .__main__ import init # NOQA
import itertools
import pytest


testCV = tuple(
    'test' + ''.join(match)
    for match in itertools.product(consonants, vowels, numbers))


def test_wildcard():
    assert tuple(Wildcard('test').values) == ('test',)
    assert tuple(Wildcard('t?').values) == ('', 't')
    assert tuple(Wildcard('testCV#').values) == testCV
    assert tuple(Wildcard('test(a,b)').values) == ('testa', 'testb')
    assert tuple(Wildcard('test[ab]').values) == ('testa', 'testb')
    assert tuple(Wildcard('A').values) == alphabet
    assert tuple(Wildcard('*').values) == alphanumeric
    assert tuple(Wildcard('*?').values) == ('',) + alphanumeric
    assert tuple(Wildcard('tes(,t)?').values) == ('tes', 'test')


def test_wildcard_invalid_parentheses():
    with pytest.raises(ValueError):
        Wildcard('t(').values
    with pytest.raises(ValueError):
        Wildcard('t((').values
    with pytest.raises(ValueError):
        Wildcard('t[').values
    with pytest.raises(ValueError):
        Wildcard('t[[').values
    with pytest.raises(ValueError):
        Wildcard('t]').values
    with pytest.raises(ValueError):
        Wildcard('t)').values


def test_main_help(capsys):
    with pytest.raises(SystemExit):
        main(['-h'])
    captured = capsys.readouterr()
    assert 'usage: domainsearch' in captured.out


def test_whois_lookup(capsys):
    main(['test[ab]'])
    captured = capsys.readouterr()
    assert 'testa.com' in captured.out
    assert 'testb.com' in captured.out


def test_whois_verbose(capsys):
    main(['--verbose', 'test.com'])
    captured = capsys.readouterr()
    assert 'Registry database' in captured.out


def test_dry_run(capsys):
    main(['-n', 'testV'])
    captured = capsys.readouterr()
    out = tuple(l.strip() for l in captured.out.split('\n'))
    print(out)
    assert out == (
        'testa.com',
        'teste.com',
        'testi.com',
        'testo.com',
        'testu.com',
        '')


def test_whois_only(capsys):
    main(['--only', 'test.com'])
    captured = capsys.readouterr()
    assert captured.out == ''


def test_whois_invalid(capsys):
    main(['.com'])
    captured = capsys.readouterr()
    assert 'invalid request' in captured.out


def test_whois_avail(capsys):
    domain = 'hrkljuz34232523342.com'
    main([domain])
    captured = capsys.readouterr()
    assert '✓ ' + domain in captured.out


def test_version(capsys):
    main(['--version'])
    captured = capsys.readouterr()
    assert 'domainsearch v' in captured.out


def test_init():
    init('__main__', ['--version'])
