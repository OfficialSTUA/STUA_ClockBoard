import stua, time, export
import dotenv, os, json
from flask import Flask, render_template, Response

dotenv.load_dotenv()
stua.keyMTA(os.getenv("NYCT")) #os.getenv("NYCT"))
stua.keyBUSTIME(os.getenv("BusTime"))

#print(export.export())

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/data')
def data():
    def generate():
        value = True
        while (value == True):
            json_js = export.export()
            export.render(True)
            while (export.delay_update() != -1):
                time.sleep(1)
            return "data:" + json_js + "\n\n"
    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/rotate')
def rotate():
    def generate():
        value = True
        while (value == True):
            if (export.render() == False):
                pass
            else:
                json_str = {
                    "timer": str(export.timer()),
                    "delay_count": str(export.delay_update(current=True))
                }
                return "data:" + str(json.dumps(json_str)) + "\n\n"
    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/refresh')
def refresh():
    def generate():
        value = True
        while (value == True):
            time.sleep(0.5)
            if (export.render() == False):
                pass
            else:
                delay = export.delay_update()
                if delay == "":
                    pass
                else:
                    return "data:" + str(delay) + "\n\n"
    return Response(generate(), mimetype= 'text/event-stream')

if __name__ in "__main__":
    app.run()
