import unittest
from generate_pages import extract_title

class TestGeneratePages(unittest.TestCase):
    def test_extract_title_only(self):
        md = '# Hello'
        title = extract_title(md)
        self.assertEqual('Hello', title)

    def test_extract_title_multiple_lines(self):
        md = '''
        # Hello
        '''
        title = extract_title(md)
        self.assertEqual('Hello', title)

    def test_extract_title_other_text(self):
        md = '''
        # Hello
        ## This is a test
        #To see if it works
        With multiple lines
        '''
        title = extract_title(md)
        self.assertEqual('Hello', title)


if __name__ == '__main__':
    unittest.main()