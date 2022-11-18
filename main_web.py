import stua, time, export
import dotenv, os, json
from flask import Flask, render_template, Response

dotenv.load_dotenv()
stua.keyMTA(os.getenv("NYCT")) #os.getenv("NYCT"))
stua.keyBUSTIME(os.getenv("BusTime"))

VAR = True

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
            #try:
            json_js = export.export()
            export.render(True)
            #while ((export.delay_update() != -1)):
            #    time.sleep(0.5)
            #export.delay_lock(current=True)
            return "data:" + json_js + "\n\n"
            #except:
                #pass
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

@app.route('/delay')
def delay():
    #global VAR
    def generate():
        global VAR
        value = True
        while (value == True):
            if (export.render() == False):
                pass
            else:
                #print(VAR)
                if (export.get_timer() == False) and (VAR == True):
                    delay_get = export.delay()
                    json_str = {
                        "right_side_onedelay": {
                            "emblem": delay_get[1],
                            "delay": delay_get[2]
                        },
                        "right_side_multipledelay": {
                            "one": delay_get[3],
                            "two": delay_get[4],
                            "three": delay_get[5]
                        }
                    }
                    VAR = False
                    #print(VAR)
                    return "data:" + str(json.dumps(json_str)) + "\n\n"
                else:
                    pass

                if export.get_timer() == True:
                    VAR = True

    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/refresh')
def refresh():
    def generate():
        value = True
        while (value == True):
            if (export.render() == False):
                pass
            else:
                return "data:" + str(export.crit()) + "\n\n"
    return Response(generate(), mimetype= 'text/event-stream')

if __name__ in "__main__":
    app.run(port=5500)