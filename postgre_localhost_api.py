from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
import psycopg2

app = Flask(__name__)
api = Api(app)

conn = psycopg2.connect(database="dvdrental",
                        host="localhost",
                        user="postgres",
                        password="1432000",
                        port="5432")

cursor = conn.cursor()

class Hello(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
  
        return jsonify({'message': 'hello world'}) 
  
    # Corresponds to POST request 
    def post(self): 
          
        data = request.get_json()     # status code 
        return jsonify({'data': data}), 201

# list of actors
class ActorsInfo(Resource):
    def get(self):
        cursor.execute("SELECT * FROM public.actor ORDER BY actor_id ASC")
        rows = cursor.fetchall()
        jsonData_list = []
        for row in rows:
            jsonData_list.append({'id': row[0],'first name': row[1],'last name':row[2],'last update':row[3]})
        return jsonify(jsonData_list)

# info of one actor
class ActorInfo(Resource):
    def get(id  ):
        cursor.execute("SELECT * FROM public.actor WHERE actor_id = %s", (id,))
        rows = cursor.fetchone()
        return jsonify({'id': row[0],'first name': row[1],'last name':row[2],'last update':row[3]})
    
class Addressesinfo(Resource):
    def get(self):
        cursor.execute("SELECT * FROM public.address ORDER BY address_id ASC")
        rows = cursor.fetchall()
        jsonData_list = []
        for row in rows:
            jsonData_list.append({'id': row[0],'address': row[1],'district':row[3],'city id':row[4],'postal code':row[5],'phone':row[6],'last update':row[7]})
        return jsonify(jsonData_list)

class CountriesInfo(Resource):
    def get(self):
        cursor.execute("SELECT * FROM public.country ORDER BY country_id ASC")
        rows = cursor.fetchall()
        jsonData_list = []
        for row in rows:
            jsonData_list.append({'id': row[0],'country': row[1],'last update':row[2]})
        return jsonify(jsonData_list)

api.add_resource(Hello, '/')

api.add_resource(ActorsInfo, '/actors')
api.add_resource(ActorInfo, '/actors/<int:id>')

api.add_resource(Addressesinfo, '/addresses')
api.add_resource(CountriesInfo, '/countries')

if __name__ == '__main__':
    app.run()

# internal server error