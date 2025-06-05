import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
from htmlnode import ParentNode

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_new_lines(self):
        md = """



        This is **bolded** paragraph




        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line




        - This is a list
        - with items



        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_whitespace(self):
        md = """
           This is **bolded** paragraph        

        This is another paragraph with _italic_ text and `code` here     
               This is the same paragraph on a new line





             - This is a list     
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_type_heading(self):
        md = '# Heading1'
        type = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, type)

    def test_block_type_heading2(self):
        md = '###### Heading1'
        type = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, type)

    def test_block_type_heading_false(self):
        md = '#Heading1'
        type = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, type)

    def test_block_type_code(self):
        md = '```This is code```'
        type = block_to_block_type(md)
        self.assertEqual(BlockType.CODE, type)

    def test_block_type_quote(self):
        md = '>This is a quote'
        type = block_to_block_type(md)
        self.assertEqual(BlockType.QUOTE, type)

    def test_block_type_quote2(self):
        md = '''>This is a quote
        >On multiple lines'''
        type = block_to_block_type(md)
        self.assertEqual(BlockType.QUOTE, type)

    def test_block_type_unordered_list(self):
        md = '''- This is
        - An unordered
        - List'''
        type = block_to_block_type(md)
        self.assertEqual(BlockType.UNORDERED_LIST, type)
    
    def test_block_type_unordered_list_false(self):
        md = '''- This is not
        -An unordered
        - List'''
        type = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, type)

    def test_block_type_ordered_list(self):
        md = '''1. This is
        2. An ordered
        3. List'''
        type = block_to_block_type(md)
        self.assertEqual(BlockType.ORDERED_LIST, type)

    def test_block_type_paragraph(self):
        md = 'This is just text'
        type = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, type)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
    # This is a h1 heading
    ## followed by h2
    ### and h3

    # This is another h1 heading

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a h1 heading</h1><h2>followed by h2</h2><h3>and h3</h3><h1>This is another h1 heading</h1></div>",
        )

    def test_unordered_lists(self):
        md = """

    - This is
    - an unordered
    - list

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is</li><li>an unordered</li><li>list</li></ul></div>",
        )

    def test_ordered_lists(self):
        md = """

    1. This is
    2. an ordered
    3. list

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is</li><li>an ordered</li><li>list</li></ol></div>",
        )

    def test_quotes(self):
        md = """
    >This is a quote
    >over
    >several lines
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote over several lines</blockquote></div>",
        )

if __name__ == '__main__':
    unittest.main()