import unittest
import subprocess
import os


class MggTestCase(unittest.TestCase):

    def test_ndtest(self):
        old_path = os.path.join('doc', 'inspection_data_old.csv')
        new_path = os.path.join('doc', 'inspection_data_new.csv')
        output = subprocess.check_output(['ndtest', '--old', old_path, '--new', new_path])
        self.assertEqual(1, output.count("doesn't overlap"))
        self.assertEqual(8, output.count('overlaps 1'))
        self.assertEqual(5, output.count('overlaps 2'))
