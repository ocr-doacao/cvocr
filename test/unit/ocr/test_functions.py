#!/usr/bin/python
# -*- coding: UTF8 -*-
import unittest
import mock

import sys
import os
local = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(local, "..", "..", "..", "ocr"))
from functions import call_tesseract


class TestOcr(unittest.TestCase):
    @mock.patch('functions.call')
    def test_call_tesseract(self, mock_call):
        call_tesseract("anyFile", ".ext")
        mock_call.assert_called_with(['tesseract', '-l', 'por', '-psm', '7', 'anyFile.ext', 'anyFile'])

if __name__ == '__main__':
    unittest.main()