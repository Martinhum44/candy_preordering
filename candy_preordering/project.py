from csvs import CSVFile

candy_and_cost = {
  "toblerone": 77.3,
  "haribo":40.7,
  "hichews":74.6,
  "milka": 94.0,
  "alfajores": 52.0,
  "jollyranchers": 40.0,
  "lindors":111.0,
  "nerdgummyclusters":86.0,
  "squashies": 91.7,
  "reeses":144.0,
  "bonobon": 75.0,
  "kitkat": 112.0,
  "airheads": 55.0,
  "hellopanda": 180.0
}

candy_to_orders = {
  "toblerone": 0,
  "haribo":0,
  "hichews":0,
  "milka": 0,
  "alfajores": 0,
  "jollyranchers": 0,
  "lindors":0,
  "nerdgummyclusters":0,
  "squashies": 0,
  "reeses":0,
  "bonobon": 0,
  "kitkat": 0,
  "airheads": 0,
  "hellopanda": 0
}

def add_array(list: list) -> int:
      total = 0
      for i in list:
        total += float(i)
      return total

def converter(string):
      if string == "" or string == " ":
        return float(0)
      return float(string.replace("g",""))

if __name__ == "__main__":

    file = open("a.csv")
    file = CSVFile(file)
    print(file.get_headers())
    income = [float(number.replace("$", "")) for number in file.get_column("Total to pay") if len(number) != 0]

    total_income = add_array(income)
    total_cost = 0
    data = list(file)

    candies_ordered = file.get_column("What they want")
    amounts_ordered = [i.replace("g", "") for i in file.get_column("How much")]

    for index, candy in enumerate(candies_ordered):
      try: 
        total_cost += ((int(amounts_ordered[index])/100)*candy_and_cost[candy.lower().replace(" ", "")])
        candy_to_orders[candy.lower().replace(" ", "")] += int(amounts_ordered[index])
      except KeyError:
        print(f"Candy {candy} not found. Edit the csv file to fix.")
        exit()

    print(f"Total income: ${total_income}")
    print(f"Total cost: ${total_cost}")
    print(f"Total profit: ${round(total_income - total_cost, 1)}")
    print("")

    print("Total preordered: ")
    for key in candy_to_orders:
      print(f"{key}: {candy_to_orders[key]}g")
