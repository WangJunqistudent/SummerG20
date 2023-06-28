import re

def index_generator(content, query):
    pattern = re.compile(query, re.IGNORECASE)
    for i, line in enumerate(content.split('\n')):
        if pattern.search(line):
            yield i