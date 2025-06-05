import unittest
from textnode import TextNode, TextType, text_node_to_html_node


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


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, 'https://google.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'https://google.com', 'alt': 'This is an image'})

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, 'https://google.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {'href': 'https://google.com'})


if __name__ == '__main__':
    unittest.main()