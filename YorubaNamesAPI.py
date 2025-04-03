from scraper import YorubaNamesScraper as yns
from flask import Flask, jsonify, Response
import json

api = Flask(__name__)

@api.route('/')
def test():
    return jsonify("hello world")

@api.route('/names-by-first-character/<character>')
def  names_by_first_letter(character):
    return Response(json.dumps([{"First Letter":character},{"names":yns.names_by_first_char(character)}],ensure_ascii=False))

@api.route('/get-all-names/')
def get_all_names():
    return Response(json.dumps([yns.get_all_names()],ensure_ascii=False))

@api.route('/name-info/<name>')
def get_name_info(name):
    return Response(json.dumps([{"Name":name},{"Info":yns.get_name_info(name)}],ensure_ascii=False))


if __name__ == '__main__':
    api.run(debug=True)