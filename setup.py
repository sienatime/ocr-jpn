try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'OCR for Japanese',
    'author': 'Siena Aguayo',
    'url': 'https://github.com/dotheastro/ocr-jpn',
    'author_email': 'siena.aguayo@gmail.com',
    'version': '0.1',
    'install_requires': ['nose','pillow==2.2.1'],
    'packages': ['ocrjpn'],
    'scripts': [],
    'name': 'ocrjpn'
}

setup(**config)