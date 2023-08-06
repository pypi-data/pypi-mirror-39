# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['libaaron']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'libaaron',
    'version': '1.1.3',
    'description': 'trivial functions I like to pack along for various things',
    'long_description': 'libaaron\n========\n\nJust my library of handy functions I like to bring along.\n\n.. contents::\n\n``reify`` \n----------\n``reify`` is a decorator I stole from the Pylons project that I like to\nuse frequently.\n\nfrom the docstring:\n\n    Use as a class method decorator.  It operates almost exactly like the\n    Python ``@property`` decorator, but it puts the result of the method it\n    decorates into the instance dict after the first call, effectively\n    replacing the function it decorates with an instance variable.  It is, in\n    Python parlance, a non-data descriptor.\n\n``cached``\n----------\n\n``cached`` is a decorator that makes a property but caches its results.\nIt\'s functionally similar to reify, but it dynamically creates a\n"private" attribute to cache the result instead of messing with\ndescriptors. This approach is comppatible with slots. I love slots.\n\n``w``\n-----\n``w`` is a function that takes an iterable with a context manager (like\na file object) and yields from that iterable inside its context manager.\n\n.. code:: python\n\n  >>> # instead of this:\n  >>> with open(\'myfile.txt\') as mf:\n  ...     for line in mf:\n  ...         # do something\n  ...\n  >>> # you can do this:\n  >>> for line in w(open(\'myfile.txt\')):\n  ...     # do something\n  ...\n``flatten``\n-----------\n``flatten`` is a function that takes an iterable as an arguments and\nrecursively yields all contents from nested iterables (except strings,\nwhich are yielded as strings). The optional second argument is a\nfunction that will be used to convert any mappings into iterables before\nyielding from them (in the event you want to yield from their values or\nsomething else).\n\n``quiteinterrupt``\n------------------\n``quiteinterrupt`` is a function that adds a signal handler which\nsilences the stacktrace when the a script is stopped with a keyboard\ninterrupt. It can optionally print a message on interrupt.\n\n``DotDict``\n-----------\n``DotDict`` is a subclass of dict which allows fetching items with dot\nsyntax. Useful as an ``object_hook`` when deserializing JSON, perhaps.\n\n``PBytes``\n----------\n``PBytes`` is a subclass of ``int`` which has a ``__str__`` that shows\ninterprets it as a number of bytes and make a human readable format. It\ncan also parse a number of bytes from a string.\n\n.. code:: python\n\n  >>> print(PBytes(2134963))\n  2.0 MiB\n  >>> PBytes.from_str(\'35.8 KB\')\n  PBytes(36659)\n  >>> PBytes.from_str(\'35.8 KB\', decimal=True)\n  PBytes(35800)\n\nInternally, it\'s just an integer, so you can do any integer operations\nwith it. Note that ``from_str`` does not attempt to determine whether it\nis a binary or decimal format. Default is binary. Use ``decimal=True``\nto explicitely change the behavior.\n\nIt also has a ``human_readable`` method which returns a number and the\nunits for easily constructing alterative representations:\n\n.. code:: python\n\n  >>> PBytes(83629).human_readable()\n  (81.6689453125, \'K\')\n  >>> \'%d%s\' % PBytes(83629).human_readable()\n  \'81K\'\n  >>> \'%d%s\' % PBytes(83629).human_readable(decimal=True)\n  \'83K\'\n\n\n``Enum``\n________\nMake enum.Enum_ objects, but with nicer syntax.\n\n.. code:: Python\n\n  >>> class var(libaaron.Enum):\n  ...     foo\n  ...     bar\n  ...     baz\n  ...\n  >>> var.foo\n  <var.foo: 1>\n  >>> var.bar\n  <var.bar: 2>\n  >>> var.baz\n  <var.baz: 3>\n  >>> type(var)\n  <class \'enum.EnumMeta\'>\n\nNote that the resulting object is the same type as those created with\nenum.Enum_, not a work-alike object.\n\n\n.. _enum.Enum:\n  https://docs.python.org/3/library/enum.html#creating-an-enum\n',
    'author': 'Aaron Christianson',
    'author_email': 'ninjaaron@gmail.com',
    'url': 'https://github.com/ninjaaron/libaaron',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
