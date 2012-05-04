#!/usr/bin/python
import unittest

import lsb_release as lr

import random
import string

class TestLSBRelease(unittest.TestCase):

	def test_void(self):
		self.assertTrue('Void test')

if __name__ == '__main__':
	unittest.main()
