# pyhton-mvar

<!-- [![PyPI version](https://badge.fury.io/py/yaks.svg)](https://badge.fury.io/py/yaks) -->
[![Build Status](https://travis-ci.com/gabrik/mvar-python.svg?branch=master)](https://travis-ci.com/gabrik/mvar-python)
[![codecov](https://codecov.io/gh/gabrik/mvar-python/branch/master/graph/badge.svg)](https://codecov.io/gh/gabrik/mvar-python)


A Pyhton port of Haskell's [Control.Concurrent.MVar](https://hackage.haskell.org/package/base/docs/Control-Concurrent-MVar.html).

A MVar is a mutable location which can either be empty, or contain a value.
The location can be written to and read from safely from multiple concurrent Unix threads.