from textnode import TextType, TextNode


#Splits textnode of markdown into several textnodes
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