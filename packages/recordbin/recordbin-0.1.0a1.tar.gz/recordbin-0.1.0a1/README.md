# RecordBin Python

[![Build Status](https://travis-ci.org/gtalarico/airtable-python-wrapper.svg?branch=master)](https://travis-ci.org/gtalarico/airtable-python-wrapper)
[![codecov](https://codecov.io/gh/gtalarico/airtable-python-wrapper/branch/master/graph/badge.svg)](https://codecov.io/gh/gtalarico/airtable-python-wrapper)

Python Client for Python [RecordBin](http://www.github.com/gtalarico/recordbin)

![project-logo](https://github.com/gtalarico/recordbin/blob/master/art/logo.png)

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

## License

[MIT](https://opensource.org/licenses/MIT)
