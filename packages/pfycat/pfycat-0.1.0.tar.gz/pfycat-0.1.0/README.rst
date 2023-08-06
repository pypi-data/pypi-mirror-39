`Downloads <https://pepy.tech/project/pfycat>`__

pfycat
======

simple module for rudementary usage of gfycat-api for pythoncd de

features
--------

upload files

::

   import pfycat
   r = pfycat.Client().upload('banana.gif')

authenticate

::

   r = pfycat.Client("client_id", "client_secret").upload('banana.gif')

upload as user:

::

   r = pfycat.Client(secret.client_id, secret.client_secret, secret.username, secret.password).upload('banana.gif')

dev-notes
---------

running tests
~~~~~~~~~~~~~

::

   cd pfycat
   nano tests/secret.py #needs client_id and client_secret
   env PYTHONPATH=. ./tests/live_test.py      

playing around with rest-api
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://chrome.google.com/webstore/detail/restlet-client-rest-api-t/aejoelaoggembcahagimdiliamlcdmfm/related

push to pypi
~~~~~~~~~~~~

prepare environment:

::

   gedit ~/.pypirc
   chmod 600 ~/.pypirc
   sudo apt install pandoc twine
   pip3 install restview

upload changes to test and production:

::

   pandoc -o README.rst README.md
   ~/.local/bin/restview  --pypi-strict README.rst
   # update version in setup.py
   rm -r dist

   twine upload dist/* -r testpypi
   firefox https://testpypi.python.org/pypi/pfycat
   twine upload dist/*

test install from testpypi

::

   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pfycat --no-cache-dir --user

test installation

::

   sudo pip install pfycat --no-cache-dir --user    

related links
~~~~~~~~~~~~~

-  https://developers.gfycat.com/api/
