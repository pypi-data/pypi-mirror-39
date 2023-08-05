# Chance-exception-capturer ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

ChanceExceptionCapturer is a Python library for capturing the output of logging to be evaluated in tests.

## Installation

### Requirements
* Linux
* Python 2.7 and up

`$ pip install chance-exception-capturer`

## Usage

```python
from exception_capturer import exception_capture


try:
    raise Exception()
except Exception:
    print exception_capture()

# {'exc_info': Exception(), 'exc_type': <type 'exceptions.Exception'>, 'exc_tb': ['  File "<stdin>", line 2, in <module>\n']}
```

## Development
```
$ virtualenv exception_capturer
$ . exception_capturer/bin/activate
$ pip install -e .
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
