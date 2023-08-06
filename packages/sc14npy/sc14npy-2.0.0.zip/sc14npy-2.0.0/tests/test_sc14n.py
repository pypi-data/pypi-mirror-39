#! python2
# -*- coding: utf8 -*-

"""Some tests for `sc14n.py` the Python interface to SC14N."""

# test_sc14n.py: version 2.0.0

# ************************** LICENSE *****************************************
# Copyright (C) 2017-18 David Ireland, DI Management Services Pty Limited.
# <http://www.di-mgt.com.au/contact/> <www.cryptosys.net>
# The code in this module is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
# ****************************************************************************

import context   # Setup path to module in parent
from sc14n import *  # @UnusedWildImport
import os
import sys

_MIN_DLL_VERSION = 20000

# Show some info about the core DLL
print "DLL version =", Gen.version()
print "cwd =", os.getcwd()

if Gen.version() < _MIN_DLL_VERSION:
    raise Exception('Require DLL version ' +
                    str(_MIN_DLL_VERSION) + ' or greater')


# FILE-RELATED UTILITIES
def read_binary_file(fname):
    with open(fname, "rb") as f:
        return bytearray(f.read())


def read_text_file(fname):
    with open(fname, "rb") as f:
        return str(f.read())


def write_file(fname, data):
    with open(fname, "wb") as f:
        f.write(data)


def _print_file(fname):
    """Print contents of text file"""
    s = read_text_file(fname)
    print s


# ERROR
def disp_error(n):
    """Display details of last error."""
    s = Err.last_error()
    print "ERROR %d: %s: %s" % (n, Err.error_lookup(n), "\n" + s if s else "")


###################
# THE TESTS PROPER
###################

def test_version():
    print "DLL VERSION:", Gen.version()
    print "module_name =", Gen.module_name()
    print "compile_time =", Gen.compile_time()
    print "platform =", Gen.core_platform()
    print "licence_type =", Gen.licence_type()


def test_olamundo():
    # Compute digest value of entire file (after transforming)
    fname = "olamundo.xml"
    print "FILE:", fname
    digval = C14n.file2digest(fname)
    print "DIG:", digval
    fname = "olamundo-utf8.xml"
    print "FILE:", fname
    digval = C14n.file2digest(fname)
    print "DIG:", digval
    fname = "olamundo-utf8bom.xml"
    print "FILE:", fname
    digval = C14n.file2digest(fname)
    print "DIG:", digval

    fname = "olamundo-base.xml"
    print "FILE:", fname
    s = C14n.file2string(fname, "Signature", Tran.OMITBYTAG)
    print "EXCLUDE <Signature>:\n", s.decode('utf-8')


def test_input_examples():
    print "Testing input examples..."

    # Example 1. Excludes the first element with the tag name <Signature>
    r = C14n.file2file("c14nfile1.txt", "input.xml", "Signature", Tran.OMITBYTAG)
    assert(r)

    # Example 2. Finds and transforms the first element with the tag name <SignedInfo>
    r = C14n.file2file("c14nfile2.txt", "input.xml", "SignedInfo", Tran.SUBSETBYTAG)
    assert(r)

    # Example 3. Finds and transforms the third element with the tag name <Data>
    r = C14n.file2file("c14nfile3.txt", "input.xml", "Data[3]", Tran.SUBSETBYTAG)
    assert(r)

    # Example 4. Finds and transforms the element with attribute Id="foo"
    r = C14n.file2file("c14nfile4.txt", "input.xml", "foo", Tran.SUBSETBYID)
    assert(r)

    # Example 5. Finds and transforms the element with attribute ID="bar"
    r = C14n.file2file("c14nfile5.txt", "input.xml", "ID=bar", Tran.SUBSETBYID)
    assert(r)

    # Example 6. Excludes element with attribute Id="thesig"
    r = C14n.file2file("c14nfile6.txt", "input.xml", "thesig", Tran.OMITBYID)
    assert(r)

    print "...done input examples."


def test_input_to_digest():
    print "Testing input examples to digest..."

    # Same as test_input_examples() except output diget value directly...

    # Example 1. Excludes the first element with the tag name <Signature>
    digval = C14n.file2digest("input.xml", "Signature", Tran.OMITBYTAG)
    print "DIG1 =", digval
    assert(len(digval) > 0)

    # Example 2. Finds and transforms the first element with the tag name <SignedInfo>
    digval = C14n.file2digest("input.xml", "SignedInfo", Tran.SUBSETBYTAG)
    print "DIG2 =", digval
    assert(len(digval) > 0)

    # Example 3. Finds and transforms the third element with the tag name <Data>
    digval = C14n.file2digest("input.xml", "Data[3]", Tran.SUBSETBYTAG)
    print "DIG3 =", digval
    assert(len(digval) > 0)

    # Example 4. Finds and transforms the element with attribute Id="foo"
    digval = C14n.file2digest("input.xml", "foo", Tran.SUBSETBYID)
    print "DIG4 =", digval
    assert(len(digval) > 0)

    # Example 5. Finds and transforms the element with attribute ID="bar"
    digval = C14n.file2digest("input.xml", "ID=bar", Tran.SUBSETBYID)
    print "DIG5 =", digval
    assert(len(digval) > 0)

    # Example 6. Excludes element with attribute Id="thesig"
    digval = C14n.file2digest("input.xml", "thesig", Tran.OMITBYID)
    print "DIG6 =", digval
    assert(len(digval) > 0)

    print "Expecting DIG3==DIG4 and DIG1==DIG6 in above results."


def test_exclusive():
    print "Examples from Section 2.2 of Exclusive XML Canonicalization Version 1.0 [RFC 3741]..."

    fname = "example1.xml"
    oname = "example1-incl-out.xml"
    print "FILE: ", fname
    print "Using inclusive c14n:"
    r = C14n.file2file(oname, fname, "n1:elem2", Tran.SUBSETBYTAG)
    assert(r)
    s = C14n.file2string(fname, "n1:elem2", Tran.SUBSETBYTAG)
    assert(len(s) > 0)
    print s
    digval = C14n.file2digest(fname, "n1:elem2", Tran.SUBSETBYTAG)
    digok = "RSTxYngjk7kroYxpMtbJP2g7Q3s="
    print "SHA1(subset) =", digval
    print "Correct SHA1 =", digok
    assert(digval == digok)

    fname = "example2.xml"
    oname = "example2-incl-out.xml"
    print "FILE: ", fname
    print "Using inclusive c14n:"
    r = C14n.file2file(oname, fname, "n1:elem2", Tran.SUBSETBYTAG)
    assert(r)
    s = C14n.file2string(fname, "n1:elem2", Tran.SUBSETBYTAG)
    assert(len(s) > 0)
    print s
    digval = C14n.file2digest(fname, "n1:elem2", Tran.SUBSETBYTAG)
    digok = "x9seNaaK3lTVs9n2WIIrIgDDU1E="
    print "SHA1(subset) =", digval
    print "Correct SHA1 =", digok
    assert(digval == digok)

    # Use exclusive method - outputs should be identical
    fname = "example1.xml"
    oname = "example1-excl-out.xml"
    print "FILE: ", fname
    print "Using exclusive c14n:"
    r = C14n.file2file(oname, fname, "n1:elem2", Tran.SUBSETBYTAG, TranMethod.EXCLUSIVE)
    assert(r)
    s = C14n.file2string(fname, "n1:elem2", Tran.SUBSETBYTAG, TranMethod.EXCLUSIVE)
    assert(len(s) > 0)
    print s
    digval = C14n.file2digest(fname, "n1:elem2", Tran.SUBSETBYTAG, TranMethod.EXCLUSIVE)
    digok = "qYwgpdgV1/b3PQ3aSpMx9wKGtqY="
    print "SHA1(subset) =", digval
    print "Correct SHA1 =", digok
    assert(digval == digok)

    fname = "example2.xml"
    oname = "example2-excl-out.xml"
    print "FILE: ", fname
    print "Using exclusive c14n:"
    r = C14n.file2file(oname, fname, "n1:elem2", Tran.SUBSETBYTAG, TranMethod.EXCLUSIVE)
    assert(r)
    s = C14n.file2string(fname, "n1:elem2", Tran.SUBSETBYTAG, TranMethod.EXCLUSIVE)
    assert(len(s) > 0)
    print s
    digval = C14n.file2digest(fname, "n1:elem2", Tran.SUBSETBYTAG, TranMethod.EXCLUSIVE)
    digok = "qYwgpdgV1/b3PQ3aSpMx9wKGtqY="
    print "SHA1(subset) =", digval
    print "Correct SHA1 =", digok
    assert(digval == digok)


def test_prefixlist():
    # Show use of PrefixList with excl-c14n
    fname = "soap-ts3-signed-by-alice.xml"
    print "FILE: ", fname
    print "Using exclusive c14n with PrefixList..."
    '''
    <ds:Reference URI="#TS-3">
    <ds:Transforms>
    <ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#">
    <ec:InclusiveNamespaces PrefixList="wsse SOAP-ENV" xmlns:ec="http://www.w3.org/2001/10/xml-exc-c14n#" />
    </ds:Transform>
    </ds:Transforms>
    <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256" />   
    '''
    # Transform element with wsu:Id="TS-3" using excl-c14n with PrefixList="wsse SOAP-ENV"
    s = C14n.file2string(fname, "wsu:Id=TS-3", Tran.SUBSETBYID, TranMethod.EXCLUSIVE, "wsse SOAP-ENV")
    assert(len(s) > 0)
    print s
    # Compute SHA-256 digest (to be inserted into <DigestValue> element)
    digok = "a4cojI7ZDOI1lKvGD7OHNus7qy1DQgpqNdGZ/YEDJQo="
    digval = C14n.file2digest(fname, "wsu:Id=TS-3", Tran.SUBSETBYID, DigAlg.SHA256, TranMethod.EXCLUSIVE, "wsse SOAP-ENV")
    assert(len(digval) > 0)
    print "SHA256(#TS-3)  =", digval
    print "Correct SHA256 =", digok
    assert(digval == digok)
    # Transform SignedInfo using excl-c14n with PrefixList="SOAP-ENV"
    # We can use this digest value to compute the required signature value.
    '''
    <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#">
    <ec:InclusiveNamespaces PrefixList="SOAP-ENV" xmlns:ec="http://www.w3.org/2001/10/xml-exc-c14n#" />
    </ds:CanonicalizationMethod>
    '''
    digok = "VenfIoZjs3/LxtvQdQuHIizR3vKi7TViE1ZF7Ddnn8I="
    digval = C14n.file2digest(fname, "ds:SignedInfo", Tran.SUBSETBYTAG, DigAlg.SHA256, TranMethod.EXCLUSIVE, "SOAP-ENV")
    assert(len(digval) > 0)
    print "SHA256(ds:SignedInfo)  =", digval
    print "Correct SHA256         =", digok
    assert(digval == digok)

def main():
    # test_version()
    # test_olamundo()
    # test_input_examples()
    # test_input_to_digest()
    # test_exclusive()
    test_prefixlist()

    print "ALL DONE."


if __name__ == "__main__":
    main()
