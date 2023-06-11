from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "MystudentFlat_test"

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

mysql = MySQL(app)

@app.route("/appartments", methods=['GET'], strict_slashes=False)
def get_all_flats():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM appartment''')
    results = cur.fetchall()
    colonne_names = [i[0] for i in cur.description] # Récupérer les noms de colonnes
    flats = [dict(zip(colonne_names, row)) for row in results] # Créer un dictionnaire pour chaque ligne avec les noms de colonnes comme clés

    list_all_flats = []
    for flat in flats:
        flat_id = flat['id'] # ID de l'appartement
        response_data = {
            "apppartment": flat,
            "informations": {
                "amenities": fetch_data(cur=cur, table="amenities", flat_id=flat_id),
                "additional_surfaces" : fetch_data(cur=cur, table="additional_surfaces", flat_id=flat_id),
                "building_characteristics" : fetch_data(cur=cur, table="building_characteristics", flat_id=flat_id),
                "lease_rent_charges": fetch_data(cur=cur, table="lease_rent_charges", flat_id=flat_id),
                "pictures": fetch_data(cur=cur, table="pictures", flat_id=flat_id),
                "property_characteristics": fetch_data(cur=cur, table="property_characteristics", flat_id=flat_id)
            }
        }
        list_all_flats.append(response_data)
    return jsonify(list_all_flats)

@app.route("/appartment/<id>", methods=['GET'], strict_slashes=False)
@cross_origin()
def get_flat(id):
    cur = mysql.connection.cursor()

    # Fetch appartment data
    cur.execute("SELECT * FROM appartment WHERE id=%s", (id,))
    appartment_results = cur.fetchall()
    appartment_col_names = [i[0] for i in cur.description]  # Get column names
    informations =  {
        "amenities": fetch_data(cur=cur, table="amenities", flat_id=id),
        "additional_surfaces" : fetch_data(cur=cur, table="additional_surfaces", flat_id=id),
        "building_characteristics" : fetch_data(cur=cur, table="building_characteristics", flat_id=id),
        "lease_rent_charges": fetch_data(cur=cur, table="lease_rent_charges", flat_id=id),
        "pictures": fetch_data(cur=cur, table="pictures", flat_id=id),
        "property_characteristics": fetch_data(cur=cur, table="property_characteristics", flat_id=id)
        }
    appartment_data = [dict(zip(appartment_col_names, row)) for row in appartment_results][0]

    response_data = {
    "apppartment": appartment_data,
    'information': informations
    }
    return jsonify(response_data)

def fetch_data(cur, table, flat_id):
    cur.execute(f"SELECT * FROM {table} WHERE flat_id = %s", (flat_id,))
    results = cur.fetchall()
    colonne_names = [i[0] for i in cur.description] # Récupérer les noms de colonnes
    data = [dict(zip(colonne_names, row)) for row in results][0]# Créer un dictionnaire pour chaque ligne avec les noms de colonnes comme clés
    return data
    
if __name__ == '__main__':
    app.run()