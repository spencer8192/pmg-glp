#!/usr/bin/env python3

import unittest
import os
import filecmp
from combine import combine

class TestCombine(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir('test_data')
        except FileExistsError:
            pass
        with open('test_data/test_empty.csv', 'w') as f:
            pass
        with open('test_data/file0.csv', 'w') as f:
            print('"column1"', file=f)
            print('"test0_row1', file=f)
        with open('test_data/file1.csv', 'w') as f:
            print('"column1"', file=f)
            print('"test0_row2', file=f)
        with open('test_data/test1_key.csv', 'w') as f:
            print('"column1","filename"', file=f)
            print('test0_row1,file0.csv', file=f)
        with open('test_data/test2_key.csv', 'w') as f:
            print('"column1","filename"', file=f)
            print('test0_row1,file0.csv', file=f)
            print('test0_row2,file1.csv', file=f)
        with open('test_data/file2.csv', 'w') as f:
            print('"column2"', file=f)
            print('"test_different_row1', file=f)

    def test_empty_file(self):
        # Try combining a single empty csv file (no header)
        with self.assertRaises(Exception):
            combine(['./test_data/test_empty.csv'])
    
    def test_0_files(self):
        # Try combining an empty list of csv files
        with self.assertRaises(Exception):
            combine([])
    
    def test_1_file(self):
        # Combine one file, and make sure it is unchanged
        combine(['./test_data/file0.csv'], 
                 outfile='./test_data/test-answer.csv')
        self.assertTrue(filecmp.cmp('./test_data/test-answer.csv', './test_data/test1_key.csv'))
    
    def test_2_files(self):
        # Combine two files with compatible headers
        combine(['./test_data/file0.csv', './test_data/file1.csv'],
                outfile='./test_data/test-answer.csv')
        self.assertTrue(filecmp.cmp('./test_data/test-answer.csv', './test_data/test2_key.csv'))
    
    def test_incompatible(self):
        # Combine two files with different headers
        with self.assertRaises(Exception):
            combine(['./test_data/file0.csv', './test_data/file2.csv'],)

    
if __name__ == '__main__':
    unittest.main()