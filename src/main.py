from textnode import TextNode, TextType
import shutil
import os
from generate_pages import generate_pages_recursively

def copy2():
    src_path = 'static'
    dest_path = 'public'

    #Remove existing public folder
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    #Create new public folder
    os.makedirs(dest_path)

    #Copy all files from static to public
    copy_file(src_path, dest_path)


def copy_file(curr_path, dest_path):
    #Get objects in folder
    folder_objects = os.listdir(curr_path)

    #For every object in folder, determine if file or directory
    for object in folder_objects:
        #Work on current object
        new_src_path = os.path.join(curr_path, object)
        new_dest_path = os.path.join(dest_path, object)

        #If file, copy it
        if os.path.isfile(new_src_path):
            shutil.copy(new_src_path, new_dest_path)

        #If directory, create new directory at destination, go through contents of folder
        elif os.path.isdir(new_src_path):
            os.mkdir(new_dest_path)
            copy_file(new_src_path, new_dest_path)

def main():
    copy2()
    generate_pages_recursively('content', 'template.html', 'public')




main()