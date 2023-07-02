import stua, time, export, datetime, time, threading
import dotenv, os, json, requests, traceback, multiprocessing
from flask import Flask, render_template, Response, redirect, jsonify
import logging
from flask_cors import CORS, cross_origin

#log = logging.getLogger()

VAR = True
DATA = True
LIRR = True
REFRESH = True
DELAY = True

app = Flask(__name__)
CORS(app)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return jsonify(export.export())

@app.route('/')
@cross_origin()
def refresh():
    return Response("{data:" + str(export.refresh()) + "}\n\n", mimetype='text/json')

@app.route('/delay')
@cross_origin()
def delay():
    return Response("{data:" + str(stua.alertsSubway(planned=False)) + "}\n\n", mimetype='text/json')

@app.route('/lirr')
@cross_origin()
def lirr():
    return Response("{data:" + str(export.export_lirr()) + "}\n\n", mimetype='text/json')

@app.route('/data')
@cross_origin()
def data():
    return Response(jsonify(data=str(export.export())), mimetype='text/json')

# @app.route('/rotate')
# def rotate():
#     def generate():
#         value = True
#         while (value == True):
#             if (export.render() == False):
#                 pass
#             else:
#                 json_str = {
#                     "timer": str(export.timer()),
#                     "delay_count": str(export.delay_update(current=True))
#                 }
#                 return "data:" + str(json.dumps(json_str)) + "\n\n"
#     return Response(generate(), mimetype= 'text/event-stream')

# @app.route('/delay')
# def delay():
#     global DELAY
#     #global VAR
#     def generate():
#         global VAR
#         value = True
#         while (value == True):
#             if (export.render() == False):
#                 pass
#             else:
#                 #print(VAR)
#                 #print(export.get_timer())
#                 try:
#                     if (export.get_timer() == False) and (VAR == True):
#                         delay_get = export.delay()
#                         json_str = {
#                             "right_side_onedelay": {
#                                 "emblem": delay_get[1],
#                                 "delay": delay_get[2]
#                             },
#                             "right_side_multipledelay": {
#                                 "one": delay_get[3],
#                                 "two": delay_get[4],
#                                 "three": delay_get[5]
#                             },
#                             "delay_count": delay_get[6],
#                             "delay_num": delay_get[7]
#                         }
#                         VAR = False
#                         #print(VAR)
#                         return "data:" + str(json.dumps(json_str)) + "\n\n"
#                     else:
#                         pass

#                     if export.get_timer() == True:
#                         VAR = True
                
#                 except Exception as e:
#                     #print(e)
#                     #print(e.message)
#                     DELAY = False
                    
#                     with open("errors.txt", "a") as f:
#                         f.write(f"{datetime.datetime.now()}: {str(traceback.format_exc())}\n----------")

#     return Response(generate(), mimetype= 'text/event-stream')

# @app.route('/refresh')
# def refresh():
#     global REFRESH
#     def generate():
#         value = True
#         while (value == True):
#             #try:
#             return "data:" + str(export.refresh()) + "\n\n"
#             #except Exception as e:
#             #print(str(traceback.format_exc()))
#             #REFRESH = False
#             #print(e)
#             #print(e.message)
#             #with open("errors.txt", "a") as f:
#             #    f.write(f"{datetime.datetime.now()}: {str(traceback.format_exc())}\n----------")
#             #refresh()

#     return Response(generate(), mimetype= 'text/event-stream')

# @app.route('/lirr')
# def lirr():
#     global LIRR
#     #print("ACT")
#     def generate():
#         value = True
#         while (value == True):
#             try:
#                 if (export.render() == False):
#                     pass
#                 else:
#                     f = str(export.export_lirr())
#                     #print(f)
#                     return "data:" + str(f) + "\n\n" 
            
#             except Exception as e:
#                 LIRR = False
#                 #print(e)
#                 #print(e.message)
#                 with open("errors.txt", "a") as f:
#                     f.write(f"{datetime.datetime.now()}: {str(traceback.format_exc())}\n----------")
#     return Response(generate(), mimetype= 'text/event-stream')

# def start():
#     global LIRR
#     global REFRESH
#     global DATA
#     global DELAY
    
#     while True:
#         if LIRR == False:
#             lirr()
#             LIRR = True
#         if REFRESH == False:
#             refresh()
#             REFRESH = True
#         if DATA == False:
#             data()
#             DATA = True
#         if DELAY == False:
#             delay()
#             DELAY = True
#         #print("BRUH")
#         time.sleep(5)

# #daemon = threading.Thread(target=start, daemon=True, name='Monitor')
# #daemon.start()
def background():
    while True:
        export.export()
        export.delay_export()
        export.export_lirr()
        export.rotate()
        time.sleep(7)
        print("CYCLE")

if __name__ in "__main__":
    multiprocessing.freeze_support()
    #daemon = threading.Thread(target=background, daemon=True, name='Monitor')
    #daemon.start()
    app.run(port=7082)