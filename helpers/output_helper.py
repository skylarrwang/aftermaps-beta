"""helps with html out"""
import os

def extract_components(input_html):
    """gets components"""
    # Find the Head block
    start_head = input_html.find('<head>') + len('</head>')
    end_head = input_html.find('</head>', start_head)
    uf_head = input_html[start_head:end_head]
    head_block = format_style(uf_head)

    # Find the map body block
    start_body = input_html.find('<body>') + len('<body>')
    end_body = input_html.find('</body>', start_body)
    uf_body = input_html[start_body:end_body]
    body_block = format_body(uf_body)

    # Find the JavaScript block
    start_js = input_html.find('<script>', end_head)
    end_js = input_html.find('</script>', start_js)
    js_block = input_html[start_js:end_js + len('</script>')]

    print(head_block, body_block, js_block)
    return head_block, body_block, js_block


def format_body(body):
    """helps body formatting"""
    end_div = body.find('></div>')
    start = body[:end_div-1]
    end = body[end_div-1:]
    modified_div = start + 'class="w-100 h-80"' + end
    return f'''<div class="row m-0 vh-100">
                        <div class="col-12 px-0">
                        {modified_div}
                        </div>
                    </div>'''

def format_style(head):
    """helps with style"""
    new_width = head.replace('100.0%', '80%')
    return new_width

def modified_html(head_block, body_block, js_block):
    """helps with modified"""
    jinja_template = '''
    {% extends "layout.html" %}

    {% block title %}
        Map
    {% endblock %}

    {% block head %}
    {{ head_block }}
    {% endblock %}

    {% block main %}
    {{ body_block }}
    {% endblock %}

    {% block scripts %}
    {{ js_block }}
    {% endblock %}
    '''

    modified_html = jinja_template.replace('{{ head_block }}', head_block)
    modified_html = modified_html.replace('{{ body_block }}', body_block)
    modified_html = modified_html.replace('{{ js_block }}', js_block)
    print(modified_html)
    return modified_html

def format_home():
    """modifies home page"""
    # Get the current directory of the Python script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define display paths and home paths
    display_path = os.path.join(current_dir, '..', 'templates', 'map_display.html')
    home_path = os.path.join(current_dir, '..', 'templates', 'map_home.html')

    # Open and read in string
    with open(display_path, 'r') as file:
        uf_content = file.read()

    # Extract head, body, js components and format
    head, body, js = extract_components(uf_content)
    f_content = modified_html(head, body, js)

    # Write into home file
    with open(home_path, 'w') as file:
        file.write(f_content)
    return
