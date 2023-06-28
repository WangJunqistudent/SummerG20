import os
import re
import PyPDF2
import docx2txt
from flask import Blueprint, render_template, request, jsonify, send_file
from main import app, db
from main.models import File

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('../static/templates/index.html')

def index_files(directory_path, query):
    """
    Index files under the given directory path.
    """
    index_dir = 'index_dir'
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    schema = Schema(path=TEXT(stored=True), content=TEXT(stored=True), line_number=NUMERIC(stored=True))
    ix = create_in(index_dir, schema)
    writer = ix.writer()

    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            _, file_extension = os.path.splitext(file_path)
            if file_extension == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_number, line in enumerate(f):
                        if re.search(query, line):
                            writer.add_document(path=file_path, content=line.strip(), line_number=line_number)
            elif file_extension == '.pdf':
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfFileReader(f)
                    for page_number in range(pdf_reader.getNumPages()):
                        page = pdf_reader.getPage(page_number)
                        text = page.extractText()
                        for line_number, line in enumerate(text.split('\n')):
                            if re.search(query, line):
                                writer.add_document(path=file_path, content=line.strip(), line_number=line_number)
            elif file_extension == '.docx':
                text = docx2txt.process(file_path)
                for line_number, line in enumerate(text.split('\n')):
                    if re.search(query, line):
                        writer.add_document(path=file_path, content=line.strip(), line_number=line_number)

    writer.commit()

@main_bp.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    directory_path = request.json['directory_path']
    index_files(directory_path, query)
    results = search_files(query)
    return jsonify(results)

def search_files(query):
    index_dir = 'index_dir'
    ix = open_dir(index_dir)
    with ix.searcher() as searcher:
        parser = QueryParser('content', ix.schema)
        query = parser.parse(query)
        results = searcher.search(query, limit=None)

    results_list = []
    for hit in results:
        file = File.query.filter_by(path=hit['path']).first()
        if file:
            result = {
                'id': file.id,
                'path': file.path,
                'line_number': hit['line_number'],
                'content': hit['content']
            }
            results_list.append(result)

    return results_list

@main_bp.route('/download', methods=['POST'])
def download():
    data = request.json['data']
    file_name = 'search_results.txt'
    with open(file_name, 'w') as f:
        for item in data:
            f.write(f"{item['path']}, line {item['line_number']}: {item['content']}\n")
    return send_file(file_name, as_attachment=True, attachment_filename='search_results.txt')