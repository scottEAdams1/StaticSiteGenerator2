import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a different text node', TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode('This is a text node with the same text', TextType.BOLD)
        node2 = TextNode('This is a text node with the same text', TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node with different text', TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode('This is a text node', TextType.BOLD, 'https://www.boot.dev')
        node2 = TextNode('This is a text node', TextType.BOLD, 'https://www.boot.dev')
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode('This is a text node', TextType.BOLD, 'https://www.boot.dev')
        node2 = TextNode('This is a different text node', TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode('This is a text node', TextType.BOLD)
        string = "TextNode('This is a text node', bold)"
        self.assertNotEqual(repr(node), string)


if __name__ == '__main__':
    unittest.main()