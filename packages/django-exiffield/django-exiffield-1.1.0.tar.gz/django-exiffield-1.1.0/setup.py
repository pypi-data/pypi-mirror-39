# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['exiffield']

package_data = \
{'': ['*']}

install_requires = \
['choicesenum>=0.2.2',
 'django-jsonfield>=1.0,<2.0',
 'django>=1.11',
 'pillow>=5.0,<6.0']

setup_kwargs = {
    'name': 'django-exiffield',
    'version': '1.1.0',
    'description': 'django-exiffield extracts exif information by utilizing exiftool.',
    'long_description': "=====================\ndjango-exiffield\n=====================\n\n\n.. image:: https://img.shields.io/pypi/v/django-exiffield.svg\n    :target: https://pypi.python.org/pypi/django-exiffield\n\n.. image:: https://travis-ci.org/escaped/django-exiffield.png?branch=master\n    :target: http://travis-ci.org/escaped/django-exiffield\n    :alt: Build Status\n\n.. image:: https://coveralls.io/repos/escaped/django-exiffield/badge.png?branch=master\n    :target: https://coveralls.io/r/escaped/django-exiffield\n    :alt: Coverage\n\n.. image:: https://img.shields.io/pypi/pyversions/django-exiffield.svg\n\n.. image:: https://img.shields.io/pypi/status/django-exiffield.svg\n\n.. image:: https://img.shields.io/pypi/l/django-exiffield.svg\n\n\ndjango-exiffield extracts exif information by utilizing ``exiftool``.\n\n\nRequirements\n============\n\n- `exiftool <https://www.sno.phy.queensu.ca/~phil/exiftool/>`_\n- Python 3.6\n- Django >= 1.8\n\n\nInstallation\n============\n\n#. Install django-exiffield ::\n\n    pip install django-exiffield\n\n#. Make sure ``exiftool`` is executable from you environment.\n\n\nIntegration\n===========\n\nLet's assume we have an image Model with a single ``ImageField``.\nTo extract exif information for an attached image, add an ``ExifField``,\nspecify the name of the ``ImageField`` in the ``source`` argument ::\n\n\n   from django.db import models\n\n   from exiffield.fields import ExifField\n\n\n   class Image(models.Model):\n       image = models.ImageField()\n       exif = ExifField(\n           source='image',\n       )\n\n\nand create a migration for the new field.\nThat's it.\n\nAfter attaching an image to your ``ImageField``, the exif information is stored\nas a ``dict`` on the ``ExifField``.\nEach exif information of the dictionary consists of two keys:\n\n* ``desc``: A human readable description\n* ``val``: The value for the entry.\n\nIn the following example we access the camera model ::\n\n   image = Image.objects.get(...)\n   print(image.exif['Model'])\n   # {\n   #     'desc': 'Camera Model Name',\n   #     'val': 'DMC-GX7',\n   # }\n\nAs the exif information is encoded in a simple ``dict`` you can iterate and access\nthe values with all familiar dictionary methods.\n\n\nDenormalizing Fields\n--------------------\n\nSince the ``ExifField`` stores its data simply as text, it is not possible to filter\nor access indiviual values efficiently.\nThe ``ExifField`` provides a convinient way to denormalize certain values using\nthe ``denormalized_fields`` argument.\nIt takes a dictionary with the target field as key and a simple getter function of\ntype ``Callable[[Dict[Dict[str, str]]], Any]``.\nTo denormalize a simple value you can use the provided ``exiffield.getters.exifgetter`` ::\n\n\n   from django.db import models\n\n   from exiffield.fields import ExifField\n   from exiffield.getters import exifgetter\n\n\n   class Image(models.Model):\n       image = models.ImageField()\n       camera = models.CharField(\n           editable=False,\n           max_length=100,\n       )\n       exif = ExifField(\n           source='image',\n           denormalized_fields={\n               'camera': exifgetter('Model'),\n           },\n       )\n\n\nThere are more predefined getters in ``exiffield.getters``:\n\n``exifgetter(exif_key: str) -> str``\n    Get an unmodified exif value.\n\n``get_type() -> str``\n    Get file type, e.g. video or image\n\n``get_datetake -> Optional[datetime]``\n    Get when the file was created as ``datetime``\n\n``get_orientation  -> exiffield.getters.Orientation``\n    Get orientation of media file.\n    Possible values are ``LANDSCAPE`` and ``PORTRAIT``.\n\n``get_sequenctype -> exiffield.getters.Mode``\n    Guess if the image was taken in a sequence.\n    Possible values are ``BURST``, ``BRACKETING``, ``TIMELAPSE`` and ``SINGLE``.\n\n``get_sequencenumber -> int``\n    Get image position in a sequence.\n\n\nDevelopment\n===========\n\nThis project is using `poetry <https://poetry.eustace.io/>`_ to manage all dev dependencies.\nClone this repository and run ::\n\n   poetry develop\n\n\nto create a virtual enviroment with all dependencies.\nYou can now run the test suite using ::\n\n   poetry run pytest\n\n\nThis repository follows the `angular commit conventions <https://github.com/marionebl/commitlint/tree/master/@commitlint/config-angular>`_.\nYou can register a pre-commit hook to validate your commit messages by using\n`husky <https://github.com/typicode/husky>`_. The configurations are already in place if\nyou have nodejs installed. Just run ::\n\n   npm install\n\nand the pre-commit hook will be registered.\n",
    'author': 'Alexander Frenzel',
    'author_email': 'alex@relatedworks.com',
    'url': 'https://github.com/escaped/django-exiffield',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
