httpsig Changes
---------------

1.3.0 (2019-Nov-28)
-------------------

* Relax pycryptodome requirements (PR#14 by cveilleux)
* Ability to supply another signature header like Signature (PR#15 by rbignon)
* Fixed #2; made Signer.sign() public
* Dropped Python 3.3, added Python 3.7.

1.2.0 (2018-Mar-28)
-------------------

* Switched to pycryptodome instead of PyCrypto (PR#11 by iandouglas)
* Updated tests with the test data from Draft 8 and verified it still passes.
* Dropped official Python 3.2 support (pip dropped it so it can't be properly tested)
* Cleaned up the code to be more PEP8-like.

1.1.2 (2015-Feb-11)
-------------------

* HMAC verification is now constant-time.

1.1.1 (2015-Feb-11)
-------------------

* (pulled)

1.1.0 (2014-Jul-24)
-------------------

* Changed "(request-line)" to "(request-target)" to comply with Draft 3.

1.0.3 (2014-Jul-09)
-------------------

* Unified the default signing algo under one setting. Setting httpsig.sign.DEFAULT_SIGN_ALGORITHM changes it for all future instances.
* Handle invalid params a little better.

1.0.2 (2014-Jul-02)
-------------------

* Ensure we treat headers as ASCII strings.
* Handle a case in the authorization header where there's garbage (non-keypairs) after the method name.

1.0.1 (2014-Jul-02)
~~~~~~~~~~~~~~~~~~~

* Python 3 support (2.7 + 3.2-3.4)
* Updated tox and Travis CI configs to test the supported Python versions.
* Updated README.

1.0.0 (2014-Jul-01)
~~~~~~~~~~~~~~~~~~~
* Written against http://tools.ietf.org/html/draft-cavage-http-signatures-02
* Added "setup.py test" and tox support.
* Added sign/verify unit tests for all currently-supported algorithms.
* HeaderSigner and HeaderVerifier now share the same message-building logic.
* The HTTP method in the message is now properly lower-case.
* Resolved unit test failures.
* Updated Verifier and HeaderVerifier to handle verifying both RSA and HMAC sigs.
* Updated versioneer.
* Updated contact/author info.
* Removed stray keypair in test dir.
* Removed SSH agent support.
* Removed suport for reading keyfiles from disk as this is a huge security hole if this is used in a server framework like drf-httpsig.

1.0b1 (2014-Jun-23)
~~~~~~~~~~~~~~~~~~~~~~
* Removed HTTP version from request-line, per spec (breaks backwards compatability).
* Removed auto-generation of missing Date header (ensures client compatability).


http-signature (previous)
-------------------------

0.2.0 (unreleased)
~~~~~~~~~~~~~~~~~~

* Update to newer spec (incompatible with prior version).
* Handle `request-line` meta-header.
* Allow secret to be a PEM encoded string.
* Add test cases from spec.

0.1.4 (2012-10-03)
~~~~~~~~~~~~~~~~~~

* Account for ssh now being re-merged into paramiko: either package is acceptable (but paramiko should ideally be >= 1.8.0)

0.1.3 (2012-10-02)
~~~~~~~~~~~~~~~~~~

* Stop enabling `allow_agent` by default
* Stop requiring `ssh` package by default -- it is imported only when `allow_agent=True`
* Changed logic around ssh-agent: if one key is available, don't bother with any other authentication method
* Changed logic around key file usage: if decryption fails, prompt for password
* Bug fix: ssh-agent resulted in a nonsensical error if it found no correct keys (thanks, petervolpe)
* Introduce versioneer.py
