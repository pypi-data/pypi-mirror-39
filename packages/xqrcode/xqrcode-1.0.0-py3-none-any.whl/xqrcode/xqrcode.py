# coding:utf-8


def decode_from_url(url: str):
    import os
    import tempfile
    import requests
    from .errors import HttpException

    ir = requests.get(url)
    if ir.status_code == 200:
        # path/to/temporary_file
        path_to_file = os.path.join(tempfile.gettempdir(), 'xqrcode-{}'.format(md5(url)))

        # save temporary_file
        with open(path_to_file, 'wb') as f:
            f.write(ir.content)

        # decode
        r = decode_from_file(path_to_file=path_to_file)

        # delete temporary_file
        os.remove(path_to_file)

        return r

    else:
        raise HttpException(ir.status_code)


def decode_from_file(path_to_file: str):
    from PIL import Image
    from pyzbar import pyzbar

    # open image
    img = Image.open(path_to_file)

    # decode
    items = pyzbar.decode(img)

    # exact results, get type/data
    r = []
    for item in items:
        r.append({
            'type': item.type,
            'data': item.data.decode('utf-8'),
        })

    return r


def md5(s: str):
    import hashlib

    f = hashlib.md5()
    f.update(s.encode(encoding='utf-8'))

    return f.hexdigest()
