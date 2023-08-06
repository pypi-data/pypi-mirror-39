A Python interface to Sc14n
==============================

The utility **Sc14n** performs the C14N transformation of a straightforward XML document.

	>>> # Example 1. Excludes the first element with the tag name <Signature>
	>>> r = C14n.file2file("c14nfile1.txt", "input.xml", "Signature", Tran.EXCLUDEBYTAG)
	True
	>>> # Example 2. Finds and transforms the first element with the tag name <SignedInfo>
	>>> r = C14n.file2file("c14nfile2.txt", "input.xml", "SignedInfo", Tran.SUBSETBYTAG)
	True
	>>> # Example 3. Finds and transforms the third element with the tag name <Data>
	>>> r = C14n.file2file("c14nfile3.txt", "input.xml", "Data[3]", Tran.SUBSETBYTAG)
	True
	>>> # Example 4. Finds and transforms the element with attribute Id="foo"
	>>> r = C14n.file2file("c14nfile4.txt", "input.xml", "foo", Tran.SUBSETBYID)
	True
	>>> # Example 5. Finds and transforms the element with attribute ID="bar"
	>>> r = C14n.file2file("c14nfile5.txt", "input.xml", "ID=bar", Tran.SUBSETBYID)
	True
	>>> # Example 6. Excludes element with attribute Id="thesig"
	>>> r = C14n.file2file("c14nfile6.txt", "input.xml", "thesig", Tran.EXCLUDEBYID)
	True

For full details of all available methods and options, please see the documentation.
	
Sc14n can be used with a cryptographic library to sign XML documents using XML-DSIG.
We use our cryptographic library **CryptoSys PKI** available from
http://cryptosys.net/pki/.

System requirements
-------------------

Windows platforms with Python 2 only (at least 2.6). Python 3 is not supported. 
Requires the Windows program **Sc14n** to be installed on your system.

To carry out the cryptographic signing examples  in ``test_sc14n-pki.py`` you must also install
**CryptoSys PKI**.

Downloads
---------

+ Sc14n: http://www.di-mgt.com.au/sc14n/
+ CryptoSys PKI: http://cryptosys.net/pki/
+ cryptosyspki.py: https://pypi.python.org/pypi/cryptosyspki/


Contact
-------

For more information or to make suggestions, please contact us at
https://cryptosys.net/contact/

| David Ireland
| DI Management Services Pty Ltd
| Australia
| 10 December 2018
