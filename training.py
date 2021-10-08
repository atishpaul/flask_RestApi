from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from flask_restful import Resource, Api
from pymysql.cursors import DictCursor
import datetime;

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
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(DictCursor)
            # cursor = conn.cursor()
            cursor.execute("""select * from mydata""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def post(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            name = request.form['name']
            age = request.form['age']
            emailID = request.form['emailID']
            contactNumber = request.form['contactNumber']
            isUserActive = request.form['isUserActive']
            isUserPrime = request.form['isUserPrime']
            print(datetime.datetime.now())
            registeredAt = datetime.datetime.now()
            insert_user_cmd = """INSERT INTO mydata(name, age, emailID,contactNumber,isUserActive,isUserPrime,
            registeredAt) VALUES(%s, %s, %s, %s, %s, %s, %s) """
            cursor.execute(insert_user_cmd, (name, age, emailID, contactNumber, isUserActive, isUserPrime, registeredAt))
            conn.commit()
            response = jsonify(message='User added successfully.', id=cursor.lastrowid)
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()
            return (response)


api.add_resource(UserData, '/users', endpoint='users')

if __name__ == "__main__":
    app.run(debug=True)
