#!/usr/bin/python
import unittest

import lsb_release as lr

import random
import string

class TestLSBRelease(unittest.TestCase):

	def test_lookup_codename(self):
		# Test all versions
		for rno in lr.RELEASE_CODENAME_LOOKUP:
			cdn = lr.RELEASE_CODENAME_LOOKUP[rno]
			# Test that 1.1, 1.1r0 and 1.1.8 lead to buzz. Default is picked randomly and is not supposed to go trough
			badDefault = ''.join( [random.choice(string.letters) for i in xrange(random.randint(0,9))])
			self.assertEqual(lr.lookup_codename(rno,badDefault),cdn,'Release name `' + rno + '` is not recognized.')
			self.assertEqual(lr.lookup_codename(rno + 'r' + str(random.randint(0,9)),badDefault),cdn,'Release name `' + rno + 'r*` is not recognized.')
			self.assertEqual(lr.lookup_codename(rno + '.' + str(random.randint(0,9)),badDefault),cdn,'Release name `' + rno + '.*` is not recognized.')
			self.assertEqual(lr.lookup_codename('inexistent_release' + str(random.randint(0,9)),badDefault),badDefault,'Default release codename is not accepted.')

	def test_valid_lsb_versions(self):
		raise NotImplementedError()
	def test_check_modules_installed(self):
		raise NotImplementedError()
	def test_parse_policy_line(self):
		raise NotImplementedError()
	def test_compare_release(self):
		raise NotImplementedError()
	def test_parse_apt_policy(self):
		raise NotImplementedError()
	def test_guess_release_from_apt(self):
		raise NotImplementedError()
	def test_guess_debian_release(self):
		raise NotImplementedError()
	def test_get_lsb_information(self):
		raise NotImplementedError()
	def test_get_distro_information(self):
		raise NotImplementedError()

if __name__ == '__main__':
	unittest.main()
