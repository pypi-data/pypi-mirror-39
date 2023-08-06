lazylog-python
==============

Lazylog Python Client

Installation:
```bash
$ pipenv install lazylog-python
```

Usage:
```python
>>> import lazylog
>>> lazy = lazylog.Lazylog(channel='public/lazylog-python')
>>> lazy.log('As easy as rolling off a log')
```
