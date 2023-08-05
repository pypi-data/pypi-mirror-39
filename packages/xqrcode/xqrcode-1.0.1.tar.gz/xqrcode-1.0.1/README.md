# xqrcode

A simply QR-code decoder, from URL or a file.

## Installation
```
pip3 install xqrcode
```

## Usage
```python
import xqrcode

results = xqrcode.decode_from_url(url='image-url')
```

or:
```python
import xqrcode

results = xqrcode.decode_from_file(path_to_file='/path/to/file')
```

