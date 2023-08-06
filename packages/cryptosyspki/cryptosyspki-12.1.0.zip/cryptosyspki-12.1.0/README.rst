A Python interface to CryptoSys PKI Pro
=======================================

This is a Python interface to the **CryptoSys PKI Pro** library. 


Requires: Python 2 (2.6 or above) on Windows platforms only.
CryptoSys PKI Pro v12.1 or above must be installed.
This is available from

    http://www.cryptosys.net/pki/.


To use in Python's REPL
-----------------------


.. code-block:: python

    >>> from cryptosyspki import *
    >>> Gen.version() # "hello world!" for CryptoSys PKI
    120100
    >>> Hash.hex_from_data('abc') # compute SHA-1 hash in hex of the string 'abc'
    'a9993e364706816aba3e25717850c26c9cd0d89d'
    >>> Hash.hex_from_data('abc', Hash.Alg.SHA256)   # same but using SHA-256
    'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
    >>> h = Hash.data('abc')   # h is a byte array
    >>> print Cnv.tohex(h)     # display the byte array in hex
    A9993E364706816ABA3E25717850C26C9CD0D89D

If you don't like ``import *`` and find ``cryptosyspki`` a bit long to
type each time, try


.. code-block:: python

    >>> import cryptosyspki as pki
    >>> pki.Gen.version()
    120100
    >>> pki.__version__
    '12.1.0'


Examples
--------

Look in the file ``test\test_pki.py`` and you should find an example of use for almost every available method
(perhaps contrived somewhat so they'll work in the test environment, but you should get the idea).
See also the main Python web page https://www.cryptosys.net/pki/python.html.

Tests
-----

There is a series of tests in ``test\test_pki.py``. 

The tests require certain files to exist in the current working directory and create extra files when they run.
To manage this, ``test_pki.py`` creates a temporary subdirectory.
It requires a subdirectory ``work`` to exist in the same folder
as the ``test_pki.py`` file which should contain all the required test
files, available separately in the file ``pkiPythonTestFiles.zip``. The
test function then creates a temporary subdirectory which is deleted
automatically.

::

    test/
      test_pki.py  # this module
      pkiPythonTestFiles.zip  # spare copies
      work/        # this _must_ exist
        <all required test files>
        pki.tmp.XXXXXXXX/    # created by `setup_temp_dir()`
          <copy of all required test files>
          <files created by tests>


Contact
-------

For more information or to make suggestions, please contact us at
https://cryptosys.net/contact/

| David Ireland
| DI Management Services Pty Ltd
| Australia
| <http://www.di-mgt.com.au> <http://www.cryptosys.net>
| 16 December 2018
