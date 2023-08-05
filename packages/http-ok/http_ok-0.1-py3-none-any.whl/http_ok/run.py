from flask import Flask
from werkzeug.routing import Rule
app = Flask(__name__)
app.url_map.add(Rule('/', defaults={'path': ''}, endpoint='dummy'))
app.url_map.add(Rule('/<path:path>', endpoint='dummy-path'))


@app.endpoint('dummy')
@app.endpoint('dummy-path')
def catch_all(path):
    return 'You want path: %s' % path


def main():
    global app
    app.run()


if __name__ == '__main__':
    main()
