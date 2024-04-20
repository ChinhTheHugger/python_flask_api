import json
from flask import Flask, request, jsonify, redirect
from flask_restx import Resource, Api
from flask_restful import reqparse
from sqlalchemy import create_engine
from json import dumps
import json
import psycopg2
from datetime import datetime
import time

app = Flask(__name__)
api = Api(app)

# connect to dvdrental database of postgre server on localhost
conn = psycopg2.connect(database="dvdrental",
                        host="localhost",
                        user="postgres",
                        password="1432000",
                        port="5432")

cursor = conn.cursor()



# GET: return data
# POST: create data
# PUT, PATCH: update data
# DELETE: delete data



# list all actors
@app.route('/actors')
def all_records():
        cursor.execute('''SELECT * 
                          FROM public.actor 
                          ORDER BY actor_id ASC''')
        rows = cursor.fetchall()
        jsonData_list = []
        for row in rows:
            jsonData_list.append({'_id': row[0],'first name': row[1],'last name':row[2],'last update':row[3]})
        return jsonify({'actors': jsonData_list})



# get one actor by id
# format = '/actor?id={value_here}'
@app.route('/actor', methods=['GET'])
def query_records():
    actor_id = request.args.get('id')
    cursor.execute('''SELECT * 
                      FROM public.actor 
                      WHERE actor_id = %s''', (actor_id,))
    row = cursor.fetchone()
    actor = {'_id': row[0],'first name': row[1],'last name':row[2],'last update':row[3]}
    return jsonify({'actor': actor})



# add new actor
@app.route('/new', methods=['GET','POST'])
def create_record():
    if request.method == 'POST':
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        cursor.execute('''INSERT INTO public.actor (first_name,last_name,last_update) 
                        VALUES (%s,%s,%s) 
                        RETURNING actor_id''', (fname, lname, datetime.today()))
        conn.commit()
        actor_id = cursor.fetchone()
        cursor.execute('''SELECT * 
                        FROM public.actor 
                        WHERE actor_id = %s''', (actor_id,))
        row = cursor.fetchone()
        conn.commit()
        actor = {'message': 'new actor added successfully','_id': row[0],'first name': row[1],'last name':row[2],'last update':row[3]}
        return jsonify({'actor': actor})
    return '''<form method="POST" action="">
                First name <input types="text" name="firstname">
                Last name <input type="text" name="lastname">
                <input type="submit">
              </form>'''



# update an actor by id
# format = '/update?id={value_here}'
@app.route('/update', methods=['GET','POST'])
def update_record():
    if request.method == 'POST':
        actor_id = request.args.get('id')
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        cursor.execute('''SELECT * 
                          FROM public.actor 
                          WHERE actor_id = %s''', (actor_id,))
        row1 = cursor.fetchone()
        cursor.execute('''UPDATE public.actor
                          SET first_name = %s, last_name = %s, last_update = %s
                          WHERE actor_id = %s''', (fname, lname, datetime.today(), actor_id))
        # conn.commit()
        time.sleep(20)
        cursor.execute('''SELECT * 
                          FROM public.actor 
                          WHERE actor_id = %s''', (actor_id,))
        row2 = cursor.fetchone()
        conn.commit()
        actor = {'message': 'actor updated successfully','_id': row2[0],'old first name': row1[1],'new first name': row2[1],'old last name': row1[2],'new last name':row2[2],'last update':row2[3]}
        return jsonify({'actor': actor})
    return '''<form method="POST" action="">
                First name <input types="text" name="firstname">
                Last name <input type="text" name="lastname">
                <input type="submit">
               </form>'''



# delete an actor by id
# format = '/delete?id={value_here}'
@app.route('/delete', methods=['GET'])
def delte_record():
    actor_id = request.args.get('id')
    cursor.execute('''DELETE FROM public.actor 
                      WHERE actor_id = %s
                      RETURNING *''', (actor_id,))
    row = cursor.fetchone()
    conn.commit()
    return jsonify({'message': 'actor deleted successfully','_id': row[0],'first name': row[1],'last name':row[2],'last update':row[3]})

#//////////////////////////////////////////

# list all actors
@api.route('/api/actors')
class ActorList(Resource):
    def get(self):
            cursor.execute('''SELECT * 
                            FROM public.actor 
                            ORDER BY actor_id ASC''')
            rows = cursor.fetchall()
            jsonData_list = []
            for row in rows:
                jsonData_list.append({'_id': row[0],'first name': row[1],'last name':row[2],'last update':row[3]})
            return jsonify(jsonData_list)



# get one actor by id
parser_get = reqparse.RequestParser()
parser_get.add_argument('id', type=int, required=False)
@api.route('/api/actor', endpoint='with-parser')
class ActorGet(Resource):
    @api.expect(parser_get)
    def get(self):
        args = parser_get.parse_args()
        actor_id = args['id']
        cursor.execute('''SELECT * 
                        FROM public.actor 
                        WHERE actor_id = %s''', (actor_id,))
        row = cursor.fetchone()
        return jsonify({'_id': row[0],'first name': row[1],'last name':row[2],'last update':row[3]})



# add new actor
parser_new = reqparse.RequestParser()
parser_new.add_argument('first name', type=str, required=True)
parser_new.add_argument('last name', type=str, required=True)
@api.route('/api/new')
class ActorNew(Resource):
    @api.expect(parser_new)
    def post(self):
        fname = parser_new.parse_args('first name')
        lname = parser_new.parse_args('last name')
        cursor.execute('''INSERT INTO public.actor (first_name,last_name,last_update) 
                        VALUES (%s,%s,%s) 
                        RETURNING actor_id''', (fname, lname, datetime.today()))
        actor_id = cursor.fetchone()
        cursor.execute('''SELECT * 
                        FROM public.actor 
                        WHERE actor_id = %s''', (actor_id,))
        row = cursor.fetchone()
        return jsonify({'message': 'new actor added successfully','_id': row[0],'first name': row[1],'last name':row[2],'last update':row[3]})



# # update an actor by id
# @app.route('/api/update', methods=['GET','POST'])
# def update_record():
#     if request.method == 'POST':
#         actor_id = request.args.get('id')
#         fname = request.form.get('firstname')
#         lname = request.form.get('lastname')
#         cursor.execute('''UPDATE public.actor
#                           SET first_name = %s, last_name = %s, last_update = %s
#                           WHERE actor_id = %s''', (fname, lname, datetime.today(), actor_id))
#         cursor.execute('''SELECT * 
#                           FROM public.actor 
#                           WHERE actor_id = %s''', (actor_id,))
#         row = cursor.fetchone()
#         return jsonify({'message': 'actor updated successfully','_id': row[0],'first name': row[1],'last name':row[2],'last update':row[3]})
#     else:
#         actor_id = request.args.get('id')
#         cursor.execute('''SELECT * 
#                       FROM public.actor 
#                       WHERE actor_id = %s''', (actor_id,))
#         row = cursor.fetchone()
#         return '''<form method="POST" action="">
#                     ID <input types="text" name="id" value="''' + str(row[0]) + '''" readonly>
#                     First name <input types="text" name="firstname" value="''' + str(row[1]) + '''">
#                     Last name <input type="text" name="lastname" value="''' + str(row[2]) + '''">
#                     <input type="submit">
#                   </form>'''



# delete an actor by id
parser_delete = reqparse.RequestParser()
parser_delete.add_argument('id', type=int, required=True)
@api.route('/api/delete')
class ActorDelete(Resource):
    @api.expect(parser_delete)
    def post(self):
        actor_id = parser_delete.parse_args()
        cursor.execute('''DELETE FROM public.actor 
                        WHERE actor_id = %s
                        RETURNING *''', (actor_id,))
        row = cursor.fetchone()
        return jsonify({'message': 'actor deleted successfully','_id': row[0],'first name': row[1],'last name':row[2],'last update':row[3]})



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.2')