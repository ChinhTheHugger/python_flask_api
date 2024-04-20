from flask import Flask, request
from flask_restx import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import json
from flask import jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# connect to local server
conn = psycopg2.connect(database="dvdrental",
                        host="localhost",
                        user="postgres",
                        password="1432000",
                        port="5432")



cursor = conn.cursor()

@api.route('/hello')
class Hello(Resource): 
    def get(self): 
  
        return jsonify({'message': 'hello world'}) 

# list of actors
@api.route('/actors')
class ActorsInfo(Resource):
    def get(self):
        cursor.execute('''SELECT * 
                          FROM public.actor 
                          ORDER BY actor_id ASC''')
        rows = cursor.fetchall()
        jsonData_list = []
        for row in rows:
            jsonData_list.append({'_id': row[0],'first name': row[1],'last name':row[2],'last update':row[3]})
        return jsonify(jsonData_list)

# info of one actor
@api.route('/actors/<int:actor_id>')
class ActorInfo(Resource):
    def get(self,actor_id):
        cursor.execute('''SELECT * 
                          FROM public.actor 
                          WHERE actor_id = %s''', (actor_id,))
        row = cursor.fetchone()
        return jsonify({'_id': row[0],'first name': row[1],'last name':row[2],'last update':row[3]})
    
# add new actor
@api.route('/add_actor', methods=['GET','POST'])
class ActorNew(Resource):
    def post():
        temperature = request.form.get('first name')
        room_id = request.form.get('last name')
        with conn:
            cursor.execute("INSERT INTO public.actor (first_name,last_name,last_update) VALUES (%s,%s,%s)", (room_id, temperature, datetime.today()))
        return {"message": "Temperature added."}, 201
    def get():
        return '''<form method="POST" action="">
        First name <input types="text" name="first name">
        Last name <input type="text" name="last name">
        <input type="submit">
        </form>'''
        
@app.post("/api/add")
def post():
    temperature = request.form.get('first name')
    room_id = request.form.get('last name')
    with conn:
        cursor.execute("INSERT INTO public.actor (first_name,last_name,last_update) VALUES (%s,%s,%s)", (room_id, temperature, datetime.today()))
    return {"message": "Temperature added."}, 201
@app.get("/api/add")
def get():
    return '''<form method="POST" action="">
    First name <input types="text" name="first name">
    Last name <input type="text" name="last name">
    <input type="submit">
    </form>'''


# # list of addresses
# @api.route('/addresses')
# class AddressesInfo(Resource):
#     def get(self):
#         cursor.execute('''SELECT * 
#                           FROM public.address 
#                           ORDER BY address_id ASC''')
#         rows = cursor.fetchall()
#         jsonData_list = []
#         for row in rows:
#             jsonData_list.append({'_id': row[0],'address': row[1], 'address 2': row[2],'district':row[3],'city id':row[4],'postal code':row[5],'phone':row[6],'last update':row[7]})
#         return jsonify(jsonData_list)

# # info of one address
# @api.route('/addresses/<int:address_id>')
# class AddressInfo(Resource):
#     def get(self,address_id):
#         cursor.execute('''SELECT * 
#                           FROM public.address 
#                           WHERE address_id = %s''', (address_id,))
#         row = cursor.fetchone()
#         return jsonify({'_id': row[0],'address': row[1], 'address 2': row[2],'district':row[3],'city id':row[4],'postal code':row[5],'phone':row[6],'last update':row[7]})

# # list of countries
# @api.route('/countries')
# class CountriesInfo(Resource):
#     def get(self):
#         cursor.execute('''SELECT * 
#                           FROM public.country 
#                           ORDER BY country_id ASC''')
#         rows = cursor.fetchall()
#         jsonData_list = []
#         for row in rows:
#             jsonData_list.append({'_id': row[0],'country': row[1],'last update':row[2]})
#         return jsonify(jsonData_list)

# # info of one country
# @api.route('/countries/<int:country_id>')
# class CountryInfo(Resource):
#     def get(self,country_id):
#         cursor.execute('''SELECT * 
#                           FROM public.country 
#                           WHERE country_id = %s''', (country_id,))
#         row = cursor.fetchone()
#         return jsonify({'_id': row[0],'country': row[1],'last update':row[2]})

# api.add_resource(Hello, '/')

# api.add_resource(ActorsInfo, '/actors')
# api.add_resource(ActorInfo, '/actors/<int:actor_id>')

# api.add_resource(AddressesInfo, '/addresses')
# api.add_resource(AddressInfo, '/addresses/<int:address_id>')

# api.add_resource(CountriesInfo, '/countries')
# api.add_resource(CountryInfo, '/countries/<int:country_id>')

if __name__ == '__main__':
    app.run(debug=True)

# NOTES:
# - No input form for adding new entry to table, currently treating the new object as one string parameter in the url, similar to the id parameter