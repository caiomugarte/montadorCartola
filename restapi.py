import app
import pprint
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import jsonify

pprint.pprint(app.acharMelhorTime(), width=10, indent=1, sort_dicts=False)
data = app.acharMelhorTime()

app = Flask(__name__)
api = Api(app)

class Times(Resource):
    def get(self):
        return {'data': data}, 200
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        
        parser.add_argument('esquemaID', required=True)  # add args
        
        args = parser.parse_args()  # parse arguments to dictionary
        
        # create new dataframe containing new values
    pass

api.add_resource(Times, '/times')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # run our Flask app