Overview
========
infi.caching encapsulates the caching mechanisms used in various Infinidat projects.
This project was splitted from infi.pyutils.lazy, while the latter is being phased out of use.

Usage
-----
Add infi.caching to your project requirements, and start using inside the code:

```python
# use infi.caching mechanisms in your project
from infi.caching import cached_function
@cached_function
def sample_cached_square(number):
    print 'Number given: %d, Number given squared: %d' % (number, number ** 2)
    return number ** 2

sample_cached_square(2)  # calling sample_cached_square with number=2 for the first time, no caching
sample_cached_square(2)  # calling sample_cached_square with number=2 for the second time, caching
```

Python 3 support is experimental and not fully tested.
