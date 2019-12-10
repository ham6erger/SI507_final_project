import unittest
from final_project import *
import os

class TestPandasDF(unittest.TestCase):
    '''Test that data works properly.'''
    testdir='./ttdir' # Name of the test directory

    def setUp(self):
        '''Create a test directory and create a few
        files that we will work with in the test cases.'''
        try:
            os.mkdir(self.testdir) # Create a test dir...
        except FileExistsError:
            pass # fooo already exists as a directory.
        os.chdir(self.testdir)

    def test_country_first(self):
        first_country_string = cdf.head(1).to_string(header=False)
        self.assertEqual(first_country_string, '0  Taiwan  TW')

    def test_wiki_first(self):
        first_wiki_string = df.head(1).to_string(header=False)
        self.assertEqual(first_wiki_string, '0  HongKong  1104.0  7448900  6747  82.07  0.8%  0.6%  1.1  0.17%  0.83  HK')

    def test_reddit_first(self):
        first_reddit_string = concat.head(1).to_string(header=False)
        self.assertEqual(first_reddit_string, '0  taiwan  Weekly Questions & Discussion Thread (December...  e7g13m  https://www.reddit.com/r/taiwan/comments/e7g13...  Maybe you have a question about traveling or l...  TW')

    def test_page(self):
        # page = 'https://en.wikipedia.org/wiki/Four_Asian_Tigers'
        self.assertEqual(page,'https://en.wikipedia.org/wiki/Four_Asian_Tigers')

    def tearDown(self):
        '''Delete the test directory.'''
        os.chdir('..') # Up a level out of tesdir.
        os.rmdir(self.testdir)

unittest.main()
