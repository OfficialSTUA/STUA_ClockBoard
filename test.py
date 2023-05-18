from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def index():
    return Response("Hello World", mimetype='text/html')

if __name__ == '__main__':
    app.run(debug=True)

#usr/bin/python3

string = """
<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
</head>
<body>
    <h1>Test</h1>
</body>
</html>
"""

print(string)