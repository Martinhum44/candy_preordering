import flask
from flask_cors import CORS
from candy_preordering.csvs import CSVFile
from candy_preordering.project import add_array

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        const candy_and_price = {
            "toblerone": 110,
            "haribo": 70,
            "hichews": 120,
            "milka": 110,
            "alfajores": 95,
            "jollyranchers": 50,
            "lindors": 120,
            "nerdgummyclusters": 100,
            "squashies": 120,
            "reeses": 170,
            "bonobon": 90,
            "kitkat": 140,
            "airheads": 70,
            "hellopanda": 200
        }
        function submit(name, candy, amount) {
    res = fetch("http://127.0.0.1:5500/preorder",{
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            person: name,
            candy,
            amount
        })
    }).then(res => res.json())
    .then((json) => {
        alert(json.message)
    })
}
    function onChange() {
        if(!candy_and_price[document.getElementById("candy").value]){
            document.getElementById("price").textContent = "Candy not found"
            return 
        }
        document.getElementById("price").textContent = "Price: "+ candy_and_price[document.getElementById("candy").value]/100*document.getElementById("amount").value
    }
    </script>
    <h1>Preorder some CANDY</h1>
    <input placeholder="name" type="text" id="name" oninput="onChange()"/>
    <input placeholder="candy" type="text" id="candy" oninput="onChange()">
    <input placeholder="amount" type="number" id="amount" oninput="onChange()">
    <h3 id="price"></h3>
    <button onclick="submit(document.getElementById('name').value, document.getElementById('candy').value, document.getElementById('amount').value)">Preorder</button>

</body>
</html>"""

app = flask.Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

candy_and_cost = {
  "toblerone": 77.3,
  "haribo": 40.7,
  "hichews": 74.6,
  "milka": 94.0,
  "alfajores": 52.0,
  "jollyranchers": 40.0,
  "lindors": 111.0,
  "nerdgummyclusters": 86.0,
  "squashies": 91.7,
  "reeses": 144.0,
  "bonobon": 75.0,
  "kitkat": 112.0,
  "airheads": 55.0,
  "hellopanda": 180.0
}

candy_and_price = {
  "toblerone": 110,
  "haribo": 70,
  "hichews": 120,
  "milka": 110,
  "alfajores": 95,
  "jollyranchers": 50,
  "lindors": 120,
  "nerdgummyclusters": 100,
  "squashies": 120,
  "reeses": 170,
  "bonobon": 90,
  "kitkat": 140,
  "airheads": 70,
  "hellopanda": 200
}

POSSIBLE_CANDIES = list(candy_and_cost.keys())
CSV_FILE = CSVFile("preorders.csv", ["person", "candy", "amount", "to_pay"])
print("NO MORE CORS")

@app.route("/preorder", methods=["POST"])  
def preorder():
    data = flask.request.get_json()
    print("Received keys:", sorted(data.keys()))

    if list(sorted(data.keys())) != ["amount", "candy", "person"]:
        return flask.jsonify({
            "success": False,
            "message": f"Must send in person, candy & amount. Sent: {', '.join(data.keys())}"
        }), 400

    if data["candy"] not in POSSIBLE_CANDIES:
        print(data)
        return flask.jsonify({
            "success": False,
            "message": f"Candy {data['candy']} not available"
        }), 400

    print(candy_and_price[data["candy"]])
    CSV_FILE.write_line(**data, to_pay=((candy_and_price[data["candy"]])/100)*int(data["amount"]))
    return flask.jsonify({"success": True, "message": "Posted candy to preorders."}), 200

@app.route("/home", methods=["GET"])
def home():
    return HTML, 200, {'Content-Type': 'text/html'}

@app.route("/analysis", methods=["GET"])
def analysis():
    mapped_columns = CSV_FILE.map_two_columns("candy", "amount")
    income = add_array(CSV_FILE.get_column("to_pay"))
    cost = 0

    for _candy, _amount in mapped_columns:
        cost += candy_and_cost[_candy]/100*float(_amount)
    profit = income - cost

    total = dict()
    print(mapped_columns)
    for _candy, _amount in mapped_columns:

        print(_candy, _candy in total.keys())
        if _candy in total.keys():
            total[_candy] += float(_amount)
        else:
            total[_candy] = float(_amount)

    return flask.jsonify({
        "total_orders": len(CSV_FILE),
        "income": income,
        "cost": cost,
        "profit": profit,
        "number_of_orders_per_candy": CSV_FILE.repeats_per_item_in_column("candy"),
        "amount_ordered_per_candy": total,
        "people_to_number_of_preorders": CSV_FILE.repeats_per_item_in_column("person")
    }), 200


if __name__ == "__main__":
    app.run(port=5500)