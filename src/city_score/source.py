from dataclasses import field
import json
import re
import os
import requests

path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(path, 'data')
if not os.path.exists(data_path):
    os.mkdir(data_path)

def decode_hex_match(match):
    hex_character = match.group(1)
    return chr(int(hex_character, 16))

class Source:
    name: str
    files: dict = field(default_factory=dict)

    @classmethod
    def open(cls, filename):
        file_path = os.path.join(path, 'data', filename)

        if not os.path.exists(file_path):
            cls.download(filename)
        
        return open(file_path)

    @classmethod
    def download(cls, filename):
        file_path = os.path.join(path, 'data', filename)

        info = cls.files[filename]
        response = requests.get(info['url'])
        content = response.text

        if start := info.get('start'):
            i = content.find(start)
            content = content[i:]

        if end := info.get('end'):
            i = content.find(end) + len(end)
            content = content[:i]

        # fix JS to JSON issues
        try:
            if file_path.endswith('.json'):
                json.loads(content)
        except json.decoder.JSONDecodeError:
            content = re.sub(r'\\x([a-f0-9]{2})', decode_hex_match, content, flags=re.IGNORECASE).replace("\\'", "'")

        with open(file_path, 'w') as file:
            file.write(content)

    @classmethod
    def populate(cls, cities):
        pass