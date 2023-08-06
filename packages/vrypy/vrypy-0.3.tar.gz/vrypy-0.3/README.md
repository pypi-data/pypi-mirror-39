# vrypy
Collection of Python utilities.

## vrypy.test.deep

Test utilities inspired by Perl [Test::Deep](https://metacpan.org/pod/Test::Deep)

    >>> from vrypy.test.deep import ignore, bag, super_dict_of

The `ignore()` for ignoring part of the structure during test comparison:

    >>> assert {'key': 'value'} == {'key': ignore()}
    >>> assert ["value1", "value2", "value3"] == ["value1", ignore(), ignore()]

The `bag(List)` for order-insensitive comparison:

    >>> assert {'key': [1, 3, 2]} == {'key': bag([1,2,3])}
    >>> assert [1,2,3,4] != bag([1,2,3])

The `super_dict_of(Dict)` for dict comparison with ignoring superfluous keys:

    >>> assert {'key': 'value', 'not interesting key': 'value'} \
    ...        == super_dict_of({'key': 'value'})
    >>> assert {'key': 'value'} != super_dict_of({'expected key': 'value'})
