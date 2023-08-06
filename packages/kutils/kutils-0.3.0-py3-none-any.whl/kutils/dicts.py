# -*- coding: utf-8 -*-
"""
dicts contains a number of special-case dictionaries.

.. testsetup:: *

   import kutils.dicts as kd
"""


class AttrDict(dict):
    """
    AttrDict represents a dictionary where the keys are represented as
    attributes.

    >>> d = kd.AttrDict(foo='bar')
    >>> d.foo
    'bar'
    >>> d['foo']
    'bar'
    """

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class NoneDict(dict):
    """
    NoneDict is a dictionary that returns ``None`` if a key
    is unavailable.

    >>> d = kd.NoneDict(foo='bar')
    >>> d['foo']
    'bar'
    >>> d['baz'] is None
    True
    """

    def __init__(self, *args, **kwargs):
        super(NoneDict, self).__init__(*args, **kwargs)

    def __getitem__(self, item):
        return self.get(item, None)


class StrDict(dict):
    """
    StrDict is a dictionary that returns an empty string if a key
    is unavailable.

    >>> d = kd.StrDict(foo='bar')
    >>> d['foo']
    'bar'
    >>> d['baz']
    ''
    """

    def __init__(self, *args, **kwargs):
        super(StrDict, self).__init__(*args, **kwargs)

    def __getitem__(self, item):
        return self.get(item, str())


class DictDict(dict):
    """
    DictDict is a dictionary that returns an empty StrDict if a key
    is unavailable. This is meant for a dictionary of dictionaries
    of string values.

    >>> d = kd.DictDict()
    >>> d['foo']
    {}
    >>> type(d['foo'])
    <class 'kutils.dicts.StrDict'>
    """

    def __init__(self, *args, **kwargs):
        super(DictDict, self).__init__(*args, **kwargs)

    def __getitem__(self, item):
        return self.get(item, StrDict())


class AttrNoneDict(AttrDict, NoneDict):
    """
    AttrNoneDict returns an AttrDict that returns None if a
    key isn't present.

    >>> d = kd.AttrNoneDict(foo='bar')
    >>> d.foo
    'bar'
    >>> d['foo']
    'bar'
    >>> d.bar is None
    True
    >>> d['bar'] is None
    True
    """

    def __init__(self, *args, **kwargs):
        super(AttrNoneDict, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        if item in self:
            return self[item]
        return None


class AttrStrDict(AttrDict, StrDict):
    """
    AttrStrDict returns an AttrDict that returns an empty string if a
    key isn't present.

    >>> d = kd.AttrStrDict(foo='bar')
    >>> d.foo
    'bar'
    >>> d['foo']
    'bar'
    >>> d.bar
    ''
    >>> d['bar']
    ''
    """

    def __init__(self, *args, **kwargs):
        super(AttrStrDict, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        if item in self:
            return self[item]
        return str()


class DictDict(dict):
    """
    DictDict is a dictionary that returns an empty AttrStrDict if a key
    is unavailable. This is meant for a dictionary of dictionaries
    of string values.

    >>> d = kd.DictDict()
    >>> d['foo']
    {}
    >>> type(d['foo'])
    <class 'kutils.dicts.AttrStrDict'>
    >>> d.foo.bar
    ''
    """

    def __init__(self, *args, **kwargs):
        super(DictDict, self).__init__(*args, **kwargs)

    def __getitem__(self, item):
        return self.get(item, AttrStrDict())

    def __getattr__(self, item):
        if item in self:
            return self[item]
        return AttrStrDict()


class AttrDictDict(AttrDict, DictDict):
    """
    AttrDictDict is a dictionary that returns an empty StrDict if a key
    is unavailable. This is meant for a dictionary of dictionaries
    of string values.

    >>> d = kd.AttrDictDict()
    >>> d.foo
    {}
    >>> d['foo']
    {}
    >>> d.foo.bar
    ''
    >>> d['foo']['bar']
    ''
    """

    def __init__(self, *args, **kwargs):
        super(AttrDictDict, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        if item in self:
            return self[item]
        return AttrStrDict()
