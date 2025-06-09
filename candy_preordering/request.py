import requests, json

msg = requests.get("http://127.0.0.1:5500/analysis")
text = json.loads(msg.text)

print(text)
print("Number of orders: ")
for candy, count in text["number_of_orders_per_candy"].items():
    print(f"{candy}: {count}")
print(f"\nTotal orders: {text['total_orders']}")

print("\nAmount ordered: ")
for candy, amount in text["amount_ordered_per_candy"].items():
    print(f"{candy}: {amount}g")

print(f"\nIncome: ${text['income']}")
print(f"Costs: ${text['cost']}")
print(f"Profit: ${text['profit']}")

print("\nPeople to number of preorders:")
for candy, amount in text["people_to_number_of_preorders"].items():
    print(f"{candy}: {amount} preorders")
