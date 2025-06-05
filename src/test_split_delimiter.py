import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a `code block` word", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        array = [TextNode("This is text with a ", TextType.TEXT),
                 TextNode("code block", TextType.CODE),
                 TextNode(" word", TextType.TEXT)
                 ]
        self.assertEqual(new_nodes, array)

    def test_split_four_parts(self):
        node = TextNode("This is text with a `code block` word and `another`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        array = [TextNode("This is text with a ", TextType.TEXT),
                 TextNode("code block", TextType.CODE),
                 TextNode(" word and ", TextType.TEXT),
                 TextNode("another", TextType.CODE)
                 ]
        self.assertEqual(new_nodes, array)

    def test_split_multiple_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode('This is a text with a **bolded phrase** in the middle', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        array = [TextNode("This is text with a ", TextType.TEXT),
                 TextNode("code block", TextType.CODE),
                 TextNode(" word", TextType.TEXT),
                 TextNode("This is a text with a ", TextType.TEXT),
                 TextNode("bolded phrase", TextType.BOLD),
                 TextNode(" in the middle", TextType.TEXT)
                 ]
        self.assertEqual(new_nodes, array)

    def test_split_nested(self):
        node = TextNode("This is an _italic and **bold** word_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        array = [TextNode("This is an ", TextType.TEXT),
                 TextNode("italic and ", TextType.ITALIC),
                 TextNode("bold", TextType.BOLD),
                 TextNode(" word", TextType.ITALIC)
                ]
        self.assertEqual(new_nodes, array)



if __name__ == '__main__':
    unittest.main()