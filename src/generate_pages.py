from block_markdown import markdown_to_html_node
import os


def extract_title(markdown):
    lines = markdown.split('\n')
    title = ''
    for line in lines:
        line = line.strip()
        if line[0:2] == '# ':
            title = line[2:]
    if title == '':
        raise Exception("No title given")
    return title


def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, 'r') as f:
        md = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = template.replace('{{ Title }}', title)
    generated_page = template.replace('{{ Content }}', html)
    with open(dest_path, 'w') as f:
        n = f.write(generated_page)


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    file_objects = os.listdir(dir_path_content)
    for object in file_objects:
        new_src_path = os.path.join(dir_path_content, object)
        new_dest_path = os.path.join(dest_dir_path, object)
        if os.path.isfile(new_src_path):
            if new_src_path[-3:] == '.md':
                new_dest_path = new_dest_path.replace('.md', '.html')
                generate_page(new_src_path, template_path, new_dest_path)
        elif os.path.isdir(new_src_path):
            os.makedirs(new_dest_path, exist_ok=True)
            generate_pages_recursively(new_src_path, template_path, new_dest_path)
    
    