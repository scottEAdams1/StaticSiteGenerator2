from textnode import TextType, TextNode
import re


#Splits TextNode of markdown into several TextNodes
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    #Loop through nodes given
    for node in old_nodes:

        num_open = 0
        num_close = 0
        start = 0
        end = 0

        for i, char in enumerate(node.text):

            #1 char delimiter e.g. `
            if len(delimiter) == 1:

                #Check to see if char is the delimiter
                if char == delimiter:

                    #If same amount of delimiters opened and closed, this new one is an opening
                    if num_open == num_close:
                        num_open += 1
                        end = i
                        new_nodes.append(TextNode(node.text[start:end], node.text_type))
                        start = i + 1

                    #If different amount of delimiters opened and closed, this new one is an closing
                    elif num_open > num_close:
                        num_close += 1
                        end = i
                        new_nodes.append(TextNode(node.text[start:end], text_type))
                        start = i + 1

            #2 char delimiter e.g. **
            elif len(delimiter) == 2 and i < len(node.text)-1:

                #Check to see if next two chars are the delimiter
                if char+node.text[i+1] == delimiter:

                    #If same amount of delimiters opened and closed, this new one is an opening
                    if num_open == num_close:
                        num_open += 1
                        end = i
                        new_nodes.append(TextNode(node.text[start:end], node.text_type))
                        start = i + 2

                    #If different amount of delimiters opened and closed, this new one is an closing
                    elif num_open > num_close:
                        num_close += 1
                        end = i
                        new_nodes.append(TextNode(node.text[start:end], text_type))
                        start = i + 2

        #Check delimiter closes
        if num_open != num_close:
            raise Exception('Closing delimiter not found')
        
        #Append final part of text
        elif node.text[start:len(node.text)] != '':
            new_nodes.append(TextNode(node.text[start:len(node.text)], node.text_type))

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


#Splits TextNode of markdown with images into several TextNodes
def split_nodes_image(old_nodes):
    new_nodes = []

    #Loop through nodes given
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        start = 0
        end = 0
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        #Loops through images in text
        for image in images:

            index = node.text.find(image[0])
            end = index
            new_nodes.append(TextNode(node.text[start:end-2], TextType.TEXT))
            start = index + 1 + len(image[0]) + 2 + len(image[1])
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
        
        #Append final part of text
        if node.text[start:len(node.text)] != '':
            new_nodes.append(TextNode(node.text[start:len(node.text)], node.text_type))

    return new_nodes


#Splits TextNode of markdown with links into several TextNodes
def split_nodes_links(old_nodes):
    new_nodes = []

    #Loop through nodes given
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        start = 0
        end = 0
        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        #Loops through links in text
        for link in links:

            index = node.text.find(link[0])
            end = index
            new_nodes.append(TextNode(node.text[start:end-1], TextType.TEXT))
            start = index + len(link[0]) + 2 + len(link[1]) + 1
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

        #Append final part of text
        if node.text[start:len(node.text)] != '':
            new_nodes.append(TextNode(node.text[start:len(node.text)], node.text_type))

    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], '`', TextType.CODE)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    return nodes