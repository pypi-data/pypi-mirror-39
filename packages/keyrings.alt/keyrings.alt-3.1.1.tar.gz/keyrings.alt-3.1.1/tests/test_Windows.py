from __future__ import print_function

import sys
import unittest

from keyrings.alt import Windows
from keyring.tests.test_backend import BackendBasicTests
from .test_file import FileKeyringTests


def is_win32_crypto_supported():
    try:
        __import__('keyrings.alt._win_crypto')
    except ImportError:
        return False
    return sys.platform in ['win32'] and sys.getwindowsversion()[-2] == 2


@unittest.skipUnless(is_win32_crypto_supported(),
                     "Need Windows")
class Win32CryptoKeyringTestCase(FileKeyringTests, unittest.TestCase):

    def init_keyring(self):
        return Windows.EncryptedKeyring()


@unittest.skipUnless(
    Windows.RegistryKeyring.viable
    and sys.version_info > (3,), "RegistryKeyring not viable")
class RegistryKeyringTestCase(BackendBasicTests, unittest.TestCase):
    def tearDown(self):
        # clean up any credentials created
        for cred in self.credentials_created:
            try:
                self.keyring.delete_password(*cred)
            except Exception as e:
                print(e, file=sys.stderr)

    def init_keyring(self):
        return Windows.RegistryKeyring()
