from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        return {'data': "beach 300th st ur moms house"}, 200  # return data and 200 OK code

api.add_resource(Users, '/')  # '/users' is our entry point

if __name__ == '__main__':
    app.run()  # run our Flask app