import requests, json

msg = requests.get("http://127.0.0.1:5500/analysis")
text = json.loads(msg.text)

print("Number of orders: ")
for candy, count in text["number_of_orders_per_candy"].items():
    print(f"{candy}: {count}")

