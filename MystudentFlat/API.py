from flask import Flask, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "MystudentFlat"
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False


mysql = MySQL(app)

@app.route("/appartments", methods=['GET'], strict_slashes=False)
def get_flats():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM appartment''')
    results = cur.fetchall()
    colonne_names = [i[0] for i in cur.description] # Take all name of the colonne
    flats = [dict(zip(colonne_names, row)) for row in results] # Create a dictionary for each row and add column names as keys
    return jsonify(flats)

if __name__ == '__main__':
    app.run()