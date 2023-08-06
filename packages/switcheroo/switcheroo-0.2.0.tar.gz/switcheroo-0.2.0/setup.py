# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['switcheroo']

package_data = \
{'': ['*']}

install_requires = \
['six>=1.11,<2.0']

setup_kwargs = {
    'name': 'switcheroo',
    'version': '0.2.0',
    'description': 'Efficient dispatch-based calling, that might be a switch statement in another language.',
    'long_description': "|Travis|_\n\n.. |Travis| image:: https://api.travis-ci.org/cjw296/switcheroo.svg?branch=master\n.. _Travis: https://travis-ci.org/cjw296/switcheroo\n\nSwitcheroo\n==========\n\nEfficient dispatch-based calling, that might be a switch statement in another language.\n\nshort usage\n~~~~~~~~~~~\n\n.. code-block:: python\n\n    from switcheroo import Switch\n\n    switch = Switch({\n        'foo': lambda x: x+1,\n    })\n\n>>> switch['foo'](1)\n2\n\n>>> switch['bar'](1)\nTraceback (most recent call last):\n...\nKeyError: 'bar'\n\n.. code-block:: python\n\n    from switcheroo import Switch, default\n\n    switch = Switch({\n        'foo': lambda x: x+1,\n        default: lambda x: x-1,\n    })\n\n>>> switch['foo'](1)\n2\n\n>>> switch['bar'](1)\n0\n\ndecorator usage\n~~~~~~~~~~~~~~~\n\n.. code-block:: python\n\n    from switcheroo import Switch\n\n    switch = Switch()\n\n    @switch.handles('foo')\n    def handle_foo(x):\n        return x+1\n\n    @switch.default\n    def handle_others(x):\n        return x-1\n\n>>> switch['foo'](1)\n2\n\n>>> switch['bar'](1)\n0\n\nclass helper usage\n~~~~~~~~~~~~~~~~~~\n\n.. code-block:: python\n\n    class MoarThingz(object):\n\n        switch = Switch()\n\n        def __init__(self, state):\n            self.state = state\n\n        @switch.handles('foo')\n        def handle_foo(self, x):\n            return self.state - x\n\n        @switch.default\n        def handle_foo(self, x):\n            return self.state + x\n\n        def dispatch(self, case, factor, x):\n            return factor * self.switch[case](self, x)\n\n>>> things = MoarThingz(3)\n>>> things.dispatch('foo', factor=1, x=1)\n2\n>>> things.dispatch('bar', factor=-1, x=2)\n-5\n\nsubclass usage\n~~~~~~~~~~~~~~\n\n.. code-block:: python\n\n    from switcheroo import Switch, handles, default\n\n    class MySwitch(Switch):\n\n        @handles('foo')\n        def handles(x):\n            return x+1\n\n        @default\n        def default(x):\n            return x-1\n\n>>> MySwitch['foo'](1)\n2\n>>> MySwitch['bar'](1)\n0\n",
    'author': 'Chris Withers',
    'author_email': 'chris@withers.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
