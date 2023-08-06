import re

import pytest

from reagex import reagex, repeated


def test_reagex_capturing():
    assert (reagex('hello {world}!', world='[a-zA-Z]+') == 'hello (?P<world>[a-zA-Z]+)!')


def test_reagex_non_capturing():
    assert (reagex('hello {_world}!', _world='[a-zA-Z]+') == 'hello (?:[a-zA-Z]+)!')


def test_reagex_with_multiple_groups():
    pattern = reagex(
        '{_address} {postcode} {city} {province}',
        _address = reagex(
            '{street} {number}',
            street = '(?:via|contrada|c/da|c.da|piazza|p.za) [a-zA-Z]+',
            number = 'snc|[0-9]+'
        ),
        postcode = '[0-9]{5}',
        city = '[A-Za-z]+',
        province = '[A-Z]{2}'
    )
    assert pattern == '(?:(?P<street>(?:via|contrada|c/da|c.da|piazza|p.za) [a-zA-Z]+) ' \
                      '(?P<number>snc|[0-9]+)) ' \
                      '(?P<postcode>[0-9]{5}) ' \
                      '(?P<city>[A-Za-z]+) ' \
                      '(?P<province>[A-Z]{2})'

    match = re.match(pattern, 'via Roma 123 12345 Napoli NA')
    assert match.groupdict() == dict(street='via Roma', number='123', postcode='12345',
                                     city='Napoli', province='NA')


def test_reagex_raises():
    with pytest.raises(KeyError):
        reagex('{pippo} {pluto}', pippo='ciao')


@pytest.mark.parametrize(
    'least, most, expected', [
        (1, None, 'patt(?:#patt)*'),
        (2, None, 'patt(?:#patt)+'),
        (3, None, 'patt(?:#patt){2,}'),
        (1, 2, 'patt(?:#patt)?'),
        (2, 2, 'patt#patt'),
        (1, 5, 'patt(?:#patt){,4}'),
        (3, 6, 'patt(?:#patt){2,5}'),
        (4, 4, 'patt(?:#patt){3}')
    ])
def test_repeated(least, most, expected):
    assert repeated('patt', '#', least, most) == expected


@pytest.mark.parametrize(
    'least, most', [
        (-1, None),
        (0, None),
        (1, 0),
        (8, 6)
    ])
def test_repeated_raises(least, most):
    with pytest.raises(ValueError):
        repeated('patt', '#', least, most)
