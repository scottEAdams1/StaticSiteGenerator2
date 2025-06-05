from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'


def block_to_block_type(block):
    #Heading
    if block[0] == '#':
        count = 0
        for i in range(min(6, len(block))):
            if block[i] == '#':
                count += 1
            elif block[i] == ' ':
                break
        if block[count] == ' ':
            return BlockType.HEADING
        
    #Code
    if block[0:3] == '```' and block[-3:] == '```':
        return BlockType.CODE
    
    #Quote
    if block[0] == '>':
        quote = True
        lines = block.split('\n')
        for line in lines:
            line = line.strip()
            if line[0] != '>':
                quote = False
                break
        if quote == True:
            return BlockType.QUOTE
        
    #Unordered list
    if block[0:2] == '- ':
        ul = True
        lines = block.split('\n')
        for line in lines:
            line = line.strip()
            if line[0:2] != '- ':
                ul = False
                break
        if ul == True:
            return BlockType.UNORDERED_LIST
        
    #Ordered list
    if block[0].isdigit() and block[1:3] == '. ':
        ol = True
        lines = block.split('\n')
        for line in lines:
            line = line.strip()
            if line[0].isdigit() and line[1:3] != '. ':
                ol = False
                break
        if ol == True:
            return BlockType.ORDERED_LIST
        
    #Paragraph
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = []
    lines1 = markdown.split('\n')
    block = ''
    for line in lines1:
        stripped_line = line.strip()
        if stripped_line == "" or \
           stripped_line.startswith("#"):
            blocks.append(block)
            block = ''
        block += line+'\n'
    blocks.append(block)
    
    final_blocks = []
    for i in range(len(blocks)):
        block = blocks[i]
        filtered_block = ''
        lines = block.split('\n')
        for j in range(len(lines)):
            line = lines[j]
            filtered_block += line.strip()
            if j < len(lines):
                filtered_block += '\n'
        filtered_block = filtered_block.strip()
        if len(filtered_block) > 0:
            final_blocks.append(filtered_block)
    return final_blocks


def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                filtered_block = block.replace('\n', ' ')
                tag = 'p'
                children = text_to_children(filtered_block)
            case BlockType.HEADING:
                count = 0
                for i in range(min(6, len(block))):
                    if block[i] == '#':
                        count += 1
                    elif block[i] == ' ':
                        break
                tag = f'h{count}'
                block = block.strip('#'*count).strip()
                children = text_to_children(block)
            case BlockType.CODE:
                tag = 'pre'
                children = [text_node_to_html_node(TextNode(block.strip('```').lstrip(), TextType.CODE))]
            case BlockType.QUOTE:
                lines = block.split('\n')
                filtered_block = ''
                for line in lines:
                    filtered_block += line[1:] + ' '
                filtered_block = filtered_block.strip()
                tag = 'blockquote'
                children = text_to_children(filtered_block)
            case BlockType.UNORDERED_LIST:
                children = []
                lines = block.split('\n')
                for line in lines:
                    line = line[2:]
                    child = LeafNode('li', line)
                    children.append(child)
                tag = 'ul'
            case BlockType.ORDERED_LIST:
                children = []
                lines = block.split('\n')
                for line in lines:
                    line = line.lstrip('0123456789')
                    line = line[2:]
                    child = LeafNode('li', line)
                    children.append(child)
                tag = 'ol'
        node = ParentNode(tag, children, None)
        nodes.append(node)
    head_node = ParentNode('div', nodes, None)
    return head_node