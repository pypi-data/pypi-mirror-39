from string import Formatter


def reagex(pattern, **group_patterns):
    """
    Utility function for writing regular expressions with many capturing groups in a readable,
    clean and hierarchical way. It is just a wrapper of ``str.format`` and it works in the same way.
    A minimal example::

        pattern = reagex(
            '{name} "{nickname}" {surname}',
            name='[A-Z][a-z]+',
            nickname='[a-z]+',
            surname='[A-Z][a-z]+'
        )

    Args:
        pattern (str):
            a pattern where you can use ``str.format`` syntax for groups ``{group_name}``.
            Groups are capturing unless they starts with ``'_'``.
            For each group in this argument, this function expects a keyword argument
            with the same name containing the pattern for the group.

        **group_patterns (str):
            patterns associated to groups; for each group in ``pattern`` of the kind
            ``{group_name}`` this function expects a keyword argument.

    Returns:
        a pattern you can pass to ``re`` functions
    """
    out = []
    formatter = Formatter()
    for literal_text, group_name, format_spec, conversion in formatter.parse(pattern):
        if literal_text:
            out.append(literal_text)
        if group_name:
            pattern = group_patterns[group_name]
            if group_name.startswith('_'):
                out.append('(?:%s)' % pattern)
            else:
                out.append('(?P<%s>%s)' % (group_name, pattern))
    return ''.join(out)


def repeated(pattern, sep, least=1, most=None):
    """
    Returns a pattern that matches a sequence of strings that match ``pattern`` separated by strings
    that match ``sep``.

    For example, for matching a sequence of ``'{key}={value}'`` pairs separated by ``'&'``, where
    key and value contains only lowercase letters::

        repeated('[a-z]+=[a-z]+', '&') == '[a-z]+=[a-z]+(?:&[a-z]+=[a-z]+)*'

    Args:
        pattern (str):
            a pattern
        sep (str):
            a pattern for the separator (usually just a character/string)
        least (int, positive):
            minimum number of strings matching ``pattern``; must be positive
        most (Optional[int]):
            maximum number of strings matching ``pattern``; must be greater or equal to ``least``

    Returns:
        a pattern

    """
    if least <= 0:
        raise ValueError('least should be positive; it is: %d' % least)
    if most is not None:
        if most < 2:
            raise ValueError('it does not make any sense to call this function with most<2:\n'
                             'for most=1, you could just write the <pattern> argument')
        if most < least:
            raise ValueError('most must be greater or equal to least')

    least_s = str(least - 1) if least > 1 else ''
    most_s = str(most - 1) if most else ''

    if most and least == most:
        if least == 2:
            return pattern + sep + pattern
        reps = '{%s}' % least_s
    else:
        reps = '{%s,%s}' % (least_s, most_s)

        if reps == '{,}':
            reps = '*'
        elif reps == '{1,}':
            reps = '+'
        elif reps == '{,1}':
            reps = '?'

    return ('{pattern}(?:{sep}{pattern}){reps}'
            .format(pattern=pattern, sep=sep, reps=reps))
