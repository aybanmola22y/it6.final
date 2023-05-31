from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "sales"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return data


@app.route("/customers", methods=["GET"])
def get_customers():
    query = """
    select * from customer
    """
    data = data_fetch("""select * from customer""")
    return make_response(jsonify(data), 200)


@app.route("/customers/<int:id>", methods=["GET"])
def get_customer_by_id(id):
    data = data_fetch("""select * from customer where customer_id = {}""".format(id))
    return make_response(jsonify(data), 200)


@app.route("/customers", methods=["POST"])
def add_actors():
    cur = mysql.connection.cursor()
    info = request.get_json()
    firstName = info["firstName"]
    lastName = info["lastName"]
    cur.execute(
        """ insert into customer (firstName, lastName) value (%s, %s)""",
        (firstName, lastName),
    )

    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "customer added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/customers/<int:id>", methods=["PUT"])
def update_actor(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    firstName = info["firstName"]
    lastName = info["lastName"]
    cur.execute(
        """
        update customer set firstName = %s, lastName = %s where customer_id = %s
    """,
        (firstName, lastName, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "customer updated successfully", "rows_affected": rows_affected}
        ),
        201,
    )


if __name__ == "__main__":
    app.run(debug=True)
