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
		# List versions in which the modules are available
		lsb_modules = {
			'cxx'		: ['3.0', '3.1', '3.2', '4.0', '4.1'],
			'desktop'	: ['3.1', '3.2', '4.0', '4.1'],
			'languages'  : ['3.2', '4.0', '4.1'],
			'multimedia' : ['3.2', '4.0', '4.1'],
			'printing'   : ['3.2', '4.0', '4.1'],
			'qt4'		: ['3.1'],
			'security'   : ['4.0','4.1'],
		}
		lsb_known_versions = ['2.0', '3.0', '3.1', '3.2', '4.0', '4.1'];
		for lsb_module in lsb_modules:
			in_versions = lsb_modules[lsb_module]
			for test_v in lsb_known_versions:
				vlv_result = lr.valid_lsb_versions(test_v,lsb_module)
				assert_text = 'valid_lsb_versions(' + test_v + ',' + lsb_module + ')'
				# For 2.0, all output 2.0 only.
				if test_v == '2.0':
					self.assertEqual(vlv_result,
									 ['2.0'],
									 assert_text)
				# For 3.0, all output 2.0 and 3.0.
				elif test_v == '3.0':
					self.assertEqual(vlv_result,
									 ['2.0', '3.0'],
									 assert_text)
				# Before appearance, it outputs all past LSB versions
				elif int(float(test_v)*10) < int(float(in_versions[0])*10):
					self.assertEqual(vlv_result,
									 [elem for elem in lsb_known_versions if int(float(elem)*10) <= int(float(test_v)*10)],
									 assert_text)
				# From appearence on, it outputs all lower versions from the in_versions
				else:
					self.assertEqual(vlv_result,
									 [elem for elem in in_versions if int(float(elem)*10) <= int(float(test_v)*10)],
									 assert_text)

	@unittest.skip('Test not implemented.')
	def test_check_modules_installed(self):
		raise NotImplementedError()

	def test_parse_policy_line(self):
		release_line = ''
		shortnames = lr.longnames.keys()
		random.shuffle(shortnames)
		longnames = {}
		for shortname in shortnames:
			longnames[lr.longnames[shortname]] = ''.join( [random.choice(string.letters) for i in xrange(random.randint(1,9))])
			release_line += shortname + '=' + longnames[lr.longnames[shortname]] + ','
		release_line = string.strip(release_line,',')
		self.assertEqual(sorted(lr.parse_policy_line(release_line)),sorted(longnames),'parse_policy_line(' + release_line + ')')

	@unittest.skip('Test not implemented.')
	def test_compare_release(self):
		raise NotImplementedError()
	@unittest.skip('Test not implemented.')
	def test_parse_apt_policy(self):
		raise NotImplementedError()
	@unittest.skip('Test not implemented.')
	def test_guess_release_from_apt(self):
		raise NotImplementedError()
	@unittest.skip('Test not implemented.')
	def test_guess_debian_release(self):
		raise NotImplementedError()
	@unittest.skip('Test not implemented.')
	def test_get_lsb_information(self):
		raise NotImplementedError()
	@unittest.skip('Test not implemented.')
	def test_get_distro_information(self):
		raise NotImplementedError()

if __name__ == '__main__':
	unittest.main()
