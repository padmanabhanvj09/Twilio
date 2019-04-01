from googletrans import Translator
import requests
import json
from flask import jsonify 
from flask import Flask,request
app = Flask(__name__)
@app.route("/translate",methods=['POST'])
def index():
    print('hello')
    src_text = request.json['src_text']
    #src_text = "welcome to other world"
    translator = Translator()
    translator.detect(src_text)
    langs = translator.detect([src_text])
    for lang in langs:
        src_lang = lang.lang
        if src_lang == 'ko':
            translated = translator.translate([src_text], dest='en')
            for translate in translated:
                dest_text = translate.text
        else:
            translated = translator.translate([src_text], dest='ta')
            for translate in translated:
                dest_text = translate.text
        print(type(dest_text))
    d = {}
    d['Return'] = dest_text
    print(d)
    return jsonify(d)

if __name__ == "__main__":
    app.run(host="192.168.1.2",port=5000)

