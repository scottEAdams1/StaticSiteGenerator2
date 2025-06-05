import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode('p', 'This is text', None, {'color': '#ffffff'})
        node2 = HTMLNode('p', 'This is text', None, {'color': '#ffffff'})
        self.assertEqual(repr(node), repr(node2))

    def test_not_eq(self):
        node = HTMLNode('p', 'This is text', None, {'color': '#ffffff'})
        node2 = HTMLNode('p', 'This is different text', None, {'color': '#ffffff'})
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode('p', 'This is text', None, {'color': '#ffffff'})
        html_prop = node.props_to_html()
        string = ' color="#ffffff"'
        self.assertEqual(html_prop, string)

    def test_repr(self):
        node = HTMLNode('p', 'This is text', None, {'color': '#ffffff'})
        string = "HTMLNode('p', 'This is text', children: None, {'color': '#ffffff'})"
        self.assertNotEqual(repr(node), string)


class TestleafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        html = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        self.assertEqual(html, '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_b(self):
        html = LeafNode("b", "This is bold!", {"color": "#ff0000"}).to_html()
        self.assertEqual(html, '<b color="#ff0000">This is bold!</b>')

    def test_leaf_to_html_no_tag(self):
        html = LeafNode(None, "This is bold!", {"color": "#ff0000"}).to_html()
        self.assertEqual(html,'This is bold!')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")


if __name__ == '__main__':
    unittest.main()