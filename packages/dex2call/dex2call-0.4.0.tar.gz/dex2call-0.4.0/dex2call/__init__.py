#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
This script takes an APK file or a DEX file and extracts all the API
calls made by methods that do not belong to classes in the android package.

By default it removes the calls made to methods that do not belong to the android.jar.
This means that the default behaviour is to get the calls made to android.jar made by
the developer's code.

(c) 2018 Daniel Domínguez <daniel.dominguez@imdea.org>
"""

from __future__ import print_function

import re
import sys
from itertools import chain
from tempfile import NamedTemporaryFile

import r2pipe
from androguard.core.bytecodes.apk import APK

IS_ANDROID_METHOD = re.compile(r'^.android\/')
IS_INVOCATION_OPCODE = re.compile(r'^invoke-')
INVOKE_DISASM = re.compile(r'^invoke-.* \{.*\}, ([^ ]*)( ;.*)?$')


def extract_called(opcodes):
    """
    Takes the called method from the disassembly and returns it.
    """
    return re.search(INVOKE_DISASM, opcodes).group(1)


def nop(_):
    pass


class Extractor(object):
    """
    This class implements the logic for extracting the API calls to android.jar from the bytecode.
    """

    def __init__(self, dexpath, pkg_name=None, android_only=True, r2_prelude=nop):
        """
        Inits all the attributes.
        """
        self.android_only = android_only
        self.dexpath = dexpath
        self.pkg_name = pkg_name
        self.r2_prelude = r2_prelude

    def extract(self):
        """
        Launches the extraction logic.
        """
        if self.dexpath.endswith('.dex'):
            if not self.pkg_name:
                raise TypeError("Expected the package name since it can't be inferred")
            return self.extract_calls_from_dex(self.dexpath)
        else:
            return self.extract_calls_from_apk(self.dexpath)

    def extract_calls_from_apk(self, apkfile):
        """
        Extracts the APK using androguard and pass each dex file to the dex extracion routine.
        """
        apk = APK(apkfile)
        self.pkg_name = apk.get_package()
        for dex in apk.get_all_dex():
            with NamedTemporaryFile(delete=True) as temp:
                temp.write(dex)
                for mthd in self.extract_calls_from_dex(temp.name):
                    yield mthd

    def extract_calls_from_dex(self, dexfile):
        """
        Using radare2 as backend extracts the method calls from the Dalvik Bytecode.

        Returns a generator and nothing is actually executed except the first 2
        commands until the generator starts to yield values.
        """
        self.r2 = r2pipe.open(dexfile) # pylint: disable=invalid-name,attribute-defined-outside-init
        self.r2_prelude(self.r2)
        self.r2.cmd('aa')

        # Take the classes that are from the package of the developer's code.
        # The command 'icj' returns each class with their methods
        interesting_classes = filter(self.class_is_from_the_pkg, self.r2.cmdj('icj'))
        # Extract the code of each method
        methods = chain(*map(self.extract_methods, interesting_classes))
        # Take the disassembly from the methods
        opcodes = (mthd['disasm'] for mthd in chain(*methods) if IS_INVOCATION_OPCODE.match(mthd['disasm']))
        # From the code of each method, extract the ones that invoke other methods
        #opcodes = filter(IS_INVOCATION_OPCODE.match, disassemblies)
        # From the disasm of each opcode, extract the called method
        called_methods = set(map(extract_called, opcodes))
        # Filter the methods that are not from android.jar
        if self.android_only:
            called_methods = filter(IS_ANDROID_METHOD.match, called_methods)

        # The method returns a generator that yields all the required methods.
        # However, if the method returns after closing the pipe to radare2, when
        # the commands used in the intermediate steps of the logic are invoked,
        # will fail because there's no radare2 instance listening on the other side.
        for mthd in called_methods:
            yield mthd
        self.r2.quit()

    def class_is_from_the_pkg(self, klass):
        """
        Returns whenever the class is from the package, this means, it's not from android.
        """
        return not IS_ANDROID_METHOD.match(klass['classname'])

    def extract_methods(self, klass):
        """
        Takes the JSON of a class and extracts the code of each method.
        """
        return map(self.parse_method, klass['methods'])

    def parse_method(self, method):
        """
        From a method JSON takes the address and returns the disasembly of the method.
        """
        mthd_result = self.r2.cmdj('pdfj @ 0x%08x' % method['addr'])
        if mthd_result:
            return mthd_result['ops']
        else:
            return []
