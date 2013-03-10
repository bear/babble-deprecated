babble
======

Purpose
-------
yes, another python bot - this one is geared to new coders

Uses the yapsy plugin framework for the bot modules and loads each module
into it's own subprocess to prevent any module from impacting the core bot
loop.

Currently the bot only works with IRC, but i'm planning to add XMPP.

Targets Python 2.7+

Dependencies
------------

- [irclib](https://github.com/python-irclib/python-irclib) by Joel Rosdahl
  It's included with this source and is also available from GitHub
- [yapsy](http://packages.python.org/Yapsy)
  Yet another plugin system
- [bearlib](https://github.com/bearlib)

License
-------
Babble is licensed as BSD, see the [LICENSE](http://github.com/bear/babble/LICENSE) file for the full text.

BSD license is described here: http://www.opensource.org/licenses/BSD-3-Clause/
