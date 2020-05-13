from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
        return ("<!DOCTYPE html>\
                <html>\
                <head>\
                <title>Hello World</title>\
                </head>\
                <body>\
                \
                <h1>Hello World</h1>\
                <p>...</p>\
                \
                </body>\
                </html>")

if __name__ == '__main__':
        app.run(host= '0.0.0.0', port = 7000, debug= True)
