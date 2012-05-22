#!/usr/bin/python
import unittest

import lsb_release as lr

import random
import string

import os

def rnd_string(min_l,max_l):
	return ''.join( [random.choice(string.letters) for i in xrange(random.randint(min_l,max_l))])

class TestLSBRelease(unittest.TestCase):

	def test_lookup_codename(self):
		# Test all versions
		for rno in lr.RELEASE_CODENAME_LOOKUP:
			cdn = lr.RELEASE_CODENAME_LOOKUP[rno]
			# Test that 1.1, 1.1r0 and 1.1.8 lead to buzz. Default is picked randomly and is not supposed to go trough
			badDefault = rnd_string(0,9)
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

	def test_check_modules_installed(self):
		# Test that when no packages are available, then we get nothing out.
		os.environ['TEST_DPKG_QUERY_NONE'] = '1'
		self.assertEqual(lr.check_modules_installed(),[])
		os.environ.pop('TEST_DPKG_QUERY_NONE')

		# Test with all packages available.
		supposed_output = [pkg[4::] + '-9.8-TESTarch' for pkg in lr.PACKAGES.split(' ')]
		supposed_output += [pkg[4::] + '-9.8-noarch' for pkg in lr.PACKAGES.split(' ')]
		supposed_output.sort()
		os.environ['TEST_DPKG_QUERY_ALL'] = '1'
		self.assertEqual(sorted(lr.check_modules_installed()),supposed_output)

	def test_parse_policy_line(self):
		release_line = ''
		shortnames = lr.longnames.keys()
		random.shuffle(shortnames)
		longnames = {}
		for shortname in shortnames:
			longnames[lr.longnames[shortname]] = rnd_string(1,9)
			release_line += shortname + '=' + longnames[lr.longnames[shortname]] + ','
		release_line = string.strip(release_line,',')
		self.assertEqual(sorted(lr.parse_policy_line(release_line)),sorted(longnames),'parse_policy_line(' + release_line + ')')

	def test_compare_release(self):
		# Test that equal suite strings lead to 0
		fake_release_equal = rnd_string(1,25)
		x = [rnd_string(1,12), {'suite': fake_release_equal}]
		y = [rnd_string(1,12), {'suite': fake_release_equal}]
		self.assertEqual(lr.compare_release(x,y),0)
		
		# Test that sequences in RELEASES_ORDER lead to reliable output
		RO_min = 0
		RO_max = len(lr.RELEASES_ORDER) - 1
		x_suite_i = random.randint(RO_min,RO_max)
		y_suite_i = random.randint(RO_min,RO_max)
		x[1]['suite'] = lr.RELEASES_ORDER[x_suite_i]
		y[1]['suite'] = lr.RELEASES_ORDER[y_suite_i]
		supposed_output = y_suite_i - x_suite_i
		self.assertEqual(lr.compare_release(x,y),
				 supposed_output,
				 'compare_release(' + x[1]['suite'] + ',' + y[1]['suite'] + ') =? ' + str(supposed_output))
		
		# Test that sequences not in RELEASES_ORDER lead to reliable output
		x[1]['suite'] = rnd_string(1,12)
		y[1]['suite'] = rnd_string(1,12)
		supposed_output = cmp(x[1]['suite'],y[1]['suite'])
		self.assertEqual(lr.compare_release(x,y),
				 supposed_output,
				 'compare_release(' + x[1]['suite'] + ',' + y[1]['suite'] + ') =? ' + str(supposed_output))

	def test_parse_apt_policy(self):
		# Test almost-empty apt-cache policy
		supposed_output = [(100, {'suite': 'now'})]
		self.assertEqual(lr.parse_apt_policy(),supposed_output)
		# Add one fake entry
		os.environ['TEST_APT_CACHE1'] = '932'
		supposed_output.append((932, {'origin': 'oRigIn', 'suite': 'SuiTe', 'component': 'C0mp0nent', 'label': 'lABel'}))
		self.assertEqual(lr.parse_apt_policy(),supposed_output)
		# Add a second fake entry, unordered
		os.environ['TEST_APT_CACHE2'] = '600'
		supposed_output.append((600, {'origin': '0RigIn', 'suite': '5uiTe', 'component': 'C03p0nent', 'label': '1ABel'}))
		self.assertEqual(lr.parse_apt_policy(),supposed_output)
		os.environ.pop('TEST_APT_CACHE1')
		os.environ.pop('TEST_APT_CACHE2')

	def test_guess_release_from_apt(self):
		os.environ['TEST_APT_CACHE1'] = '932'
		os.environ['TEST_APT_CACHE2'] = '600'
		os.environ['TEST_APT_CACHE_RELEASE'] = '512'
		supposed_output = {'origin': 'or1g1n', 'suite': 'testing', 'component': 'c0mp0nent', 'label': 'l8bel'}
		self.assertEqual(lr.guess_release_from_apt(origin='or1g1n',label='l8bel',component='c0mp0nent',ignoresuites=('c0mp0nentIgn')),supposed_output)

		# Test with a special repository (for Ports)
		supposed_output = {'origin': 'P-or1g1n', 'suite': 'sid', 'component': 'OtherComp', 'label': 'P-l8bel'}
		self.assertEqual(lr.guess_release_from_apt(origin='or1g1n',label='l8bel',component='c0mp0nent',ignoresuites=('c0mp0nentIgn'),alternate_olabels={'P-or1g1n':'P-l8bel'}),supposed_output)
		os.environ.pop('TEST_APT_CACHE1')
		os.environ.pop('TEST_APT_CACHE2')
		os.environ.pop('TEST_APT_CACHE_RELEASE')

	@unittest.skip('Test not implemented.')
	def test_guess_debian_release(self):
		raise NotImplementedError()

	def test_get_lsb_information(self):
		# Test that an inexistant /etc/lsb-release leads to empty output
		supposed_output = {}
		os.environ['LSB_ETC_LSB_RELEASE'] = 'test/inexistant_file_' + rnd_string(2,5)
		self.assertEqual(lr.get_lsb_information(),supposed_output)
		# Test that a fake /etc/lsb-release leads to output with only the content we want
		supposed_output = {'RELEASE': '(The release number)',
				   'CODENAME': '(The codename for the release)',
				   'ID': '(Distributor ID)',
				   'DESCRIPTION': '(A human-readable description of the release)'}
		os.environ['LSB_ETC_LSB_RELEASE'] = 'test/lsb-release'
		self.assertEqual(lr.get_lsb_information(),supposed_output)
		os.environ.pop('LSB_ETC_LSB_RELEASE')

	@unittest.skip('Test not implemented.')
	def test_get_distro_information(self):
		raise NotImplementedError()

if __name__ == '__main__':
	unittest.main()
