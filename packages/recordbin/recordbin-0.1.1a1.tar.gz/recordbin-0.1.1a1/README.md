# RecordBin Python

[![PyPi](https://img.shields.io/pypi/v/recordbin.svg)](https://pypi.python.org/pypi/recordbin)
[![Build Status](https://travis-ci.org/gtalarico/recordbin-python.svg?branch=master)](https://travis-ci.org/gtalarico/recordbin-python)
[![codecov](https://codecov.io/gh/gtalarico/recordbin-python/branch/master/graph/badge.svg)](https://codecov.io/gh/gtalarico/recordbin-python)

Python Client for Python [RecordBin](http://www.github.com/gtalarico/recordbin)

---

![project-logo](https://github.com/gtalarico/recordbin-python/blob/master/art/logo.png)

## Installing

```
pip install recordbin
```

### Usage Example

```
>>> from recordbin import RecordBin
>>> recordbin = RecordBin('http://ww-recordbin.herokuapp.com', token='123')
>>> recordbin.post({'username': 'gtalarico'})
```

#### Getting Posted Record

By default records are posted asynchronously and responses
are Future objects.
To get the post response use the `result()` method

```
>>> future = recordbin.post({'username': 'gtalarico'})
>>> response = future.result()
>>> record = response.json()
```

## License

[MIT](https://opensource.org/licenses/MIT)
