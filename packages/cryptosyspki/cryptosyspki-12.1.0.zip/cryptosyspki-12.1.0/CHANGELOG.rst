Revision History
-----------------

12.1.0 (2018-12-16)
^^^^^^^^^^^^^^^^^^^

* Changes to match main core module versions 12.0 and 12.1.
* Added support for RSA-PSS in RSA signatures, CMS signed-data objects and X.509 certificates.
* Added support for RSA-OAEP in RSA encryption and CMS enveloped-data objects.
* Added support for ECDSA in X.509 certificates.
* Added support for ZLIB compression.
* Added support for AES-GCM authenticated encryption.
* Added functions to read certificate strings from P7 chain files and PFX files.
* Added option for quicker single pass in ``Wipe.file()``.
* Changed parameter in ``Cms.make_sigdata_*()`` functions from ``Cms.HashAlg`` type to ``Cms.SigAlg``.


11.3.0 (2017-10-31)
^^^^^^^^^^^^^^^^^^^

* Changes to match main core module (11.3).

11.2.0 (2017-08-11)
^^^^^^^^^^^^^^^^^^^

* Synchronized cryptosyspki.py version number with main core module (11.2).
* Substantial changes to inline documentation.
* Renamed ``Rng.bytes`` to ``Rng.bytestring`` to avoid clashes with Python built-in function.
* Changed optional parameters in ``X509.cert_path_is_valid()`` and ``X509.get_cert_count_from_p7()``.


0.1.1 (2016-08-27)
^^^^^^^^^^^^^^^^^^

* Minor changes.


0.1.0 (2016-05-25)
^^^^^^^^^^^^^^^^^^

* First release of cryptosyspki.py v0.1.0.
