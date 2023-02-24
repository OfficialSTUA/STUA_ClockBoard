import stua, time, export, datetime
import dotenv, os, json, requests, traceback
from flask import Flask, render_template, Response, redirect

dotenv.load_dotenv()
stua.keyMTA(os.getenv("NYCT")) #os.getenv("NYCT"))
stua.keyBUSTIME(os.getenv("BusTime"))

VAR = True

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('mainLIRR copy.html')

@app.route('/data')
def data():
    def generate():
        value = True
        while (value == True):
            t0 = time.time()
            try:
                #export.get_annoucements()
                json_js = export.export()
                export.render(True)
                #while ((export.delay_update() != -1)):
                #    time.sleep(0.5)
                #export.delay_lock(current=True)
                t1 = time.time() - t0
                print(t1)
                return "data:" + json_js + "\n\n"
            
            except Exception as e:
                #print(e.message)
                with open("errors.txt", "a") as f:
                    f.write(f"{datetime.datetime.now()}: {str(traceback.format_exc())}\n----------")
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
                #print(export.get_timer())
                try:
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
                            },
                            "delay_count": delay_get[6],
                            "delay_num": delay_get[7]
                        }
                        VAR = False
                        #print(VAR)
                        return "data:" + str(json.dumps(json_str)) + "\n\n"
                    else:
                        pass

                    if export.get_timer() == True:
                        VAR = True
                
                except Exception as e:
                    #print(e)
                    #print(e.message)
                    
                    with open("errors.txt", "a") as f:
                        f.write(f"{datetime.datetime.now()}: {str(traceback.format_exc())}\n----------")

    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/refresh')
def refresh():
    def generate():
        value = True
        while (value == True):
            return "data:" + str(export.refresh()) + "\n\n" 

    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/lirr')
def lirr():
    def generate():
        value = True
        while (value == True):
            try:
                if (export.render() == False):
                    pass
                else:
                    return "data:" + str(export.export_lirr()) + "\n\n" 
            
            except Exception as e:
                #print(e)
                #print(e.message)
                with open("errors.txt", "a") as f:
                    f.write(f"{datetime.datetime.now()}: {str(traceback.format_exc())}\n----------")
    return Response(generate(), mimetype= 'text/event-stream')

if __name__ in "__main__":
    app.run(port=5000)