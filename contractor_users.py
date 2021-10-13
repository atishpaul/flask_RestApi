from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from flask_restful import Resource, Api
from pymysql.cursors import DictCursor
import datetime
import hashlib
import json

# Create an instance of Flask
app = Flask(__name__)

# Create an instance of MySQL
mysql = MySQL()

# Create an instance of Flask RESTful API
api = Api(app)

# Set database credentials in config.
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'digitalvarys'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

# Initialize the MySQL extension
mysql.init_app(app)


class UserData(Resource):
    # GET ALL USERS FOR EXPLORE
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(DictCursor)
            # cursor = conn.cursor()
            cursor.execute("""select id, name,  age, emailID, isUserActive, isUserPrime,availableForNewWork, city, userType, 
            registeredAt from mydata""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


class SearchedFor(Resource):
    # SEARCH BY CITY NAME
    def get(self, searched):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(DictCursor)
            # cursor = conn.cursor()
            cursor.execute("""select id, name, age, emailID, isUserActive, isUserPrime,availableForNewWork, city, userType, 
            registeredAt from mydata where city like %s""", args=[searched+'%'])
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


class SignUp(Resource):
    # THIS POST REQUEST IS FOR USER SIGNUP
    def post(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(DictCursor)
            name = request.form['name']
            age = request.form['age']
            emailID = request.form['emailID']
            contactNumber = request.form['contactNumber']
            availableForNewWork = request.form['availableForNewWork']
            isUserActive = request.form['isUserActive']
            isUserPrime = request.form['isUserPrime']
            city = request.form['city']
            password = hashlib.md5(request.form['password'].encode())
            registeredAt = datetime.datetime.now()
            insert_user_cmd = """INSERT INTO mydata(name, age, emailID,contactNumber, availableForNewWork, city, 
            isUserActive,isUserPrime,password, registeredAt) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
            cursor.execute(insert_user_cmd, (
                name, age, emailID, contactNumber, availableForNewWork, city, isUserActive, isUserPrime,
                password.hexdigest(), registeredAt))
            conn.commit()
            response = jsonify(message='User added successfully.', id=cursor.lastrowid, status='SUCCESS',
                               statusCode='200')
            response.status_code = 200
        except Exception as e:
            print(e)
            if 'Duplicate' in str(e):
                response = {'status': 'DUPLICATE_USER', 'statusCode': 400}
                response.status_code = 400
            else:
                response = jsonify('Registration failed!')
        finally:
            cursor.close()
            conn.close()
            return (response)


class loggedInData(Resource):
    # THIS IS THE USER DATA WHICH USER WILL GET AFTER LOGIN
    def get(self, email, passwords):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(DictCursor)
            # cursor = conn.cursor()
            psd = hashlib.md5(passwords.encode())
            cursor.execute(
                'select * from mydata where emailID = "{}" and password = "{}"'.format(email, psd.hexdigest()))
            rows = cursor.fetchall()
            if rows:
                return jsonify(rows)
            else:
                return {"status": "INCORRECT_CREDENTIAL", "statusCode": 400}
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


api.add_resource(UserData, '/users', endpoint='users')
api.add_resource(SignUp, '/signup', endpoint='signup')
api.add_resource(loggedInData, '/loggedinuser/<string:email>/<string:passwords>', endpoint='loggedinuser')
api.add_resource(SearchedFor, '/search/<string:searched>', endpoint='search')

if __name__ == "__main__":
    app.run(debug=True)
