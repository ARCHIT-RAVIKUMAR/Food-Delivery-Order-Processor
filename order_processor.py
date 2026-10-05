# Food Delivery Order Processor
import json

# Step 1: menu and sample orders

menu = {
    "Pizza": 250,
    "Burger": 120,
    "Biryani": 220,
    "Fries": 90,
    "Coffee": 100,
}

orders = [
    {"order_id": 1,  "customer": "Aarav",   "items": {"Pizza": 1, "Coffee": 2}},
    {"order_id": 2,  "customer": "Meera",   "items": {"Burger": 2, "Fries": 1}},
    {"order_id": 3,  "customer": "Karthik", "items": {"Biryani": 3, "Coffee": 3}},
    {"order_id": 4,  "customer": "Divya",   "items": {}},
    {"order_id": 5,  "customer": "Rahul",   "items": {"Sushi": 1}},
    {"order_id": 6,  "customer": "Priya",   "items": {"Fries": 2}},
    {"order_id": 7,  "customer": "Arjun",   "items": {"Pizza": 2, "Biryani": 2, "Coffee": 2}},
    {"order_id": 8,  "customer": "Sneha",   "items": {"Burger": 0}},
    {"order_id": 9,  "customer": "Vikram",  "items": {"Biryani": 1, "Fries": 1}},
    {"order_id": 10, "customer": "Lakshmi", "items": {"Pizza": 1, "Burger": 1, "Coffee": 1}},
    {"order_id": 11, "customer": "Nikhil",  "items": {"Coffee": 1}},
    {"order_id": 12, "customer": "Anita",   "items": {"Biryani": 4, "Burger": 2}},
]

DISCOUNT_LIMIT = 500      # discount applies above this amount
DISCOUNT_PERCENT = 10
DELIVERY_CHARGE = 40


# Step 2: core functions

def calculate_total(items):
    total = 0
    for name in items:
        quantity = items[name]
        total = total + menu[name] * quantity
    return total


def apply_discount(total):
    if total > DISCOUNT_LIMIT:
        discount = total * DISCOUNT_PERCENT / 100
    else:
        discount = 0
    return discount


def add_delivery(amount):
    return amount + DELIVERY_CHARGE


# Step 3: check for invalid orders

def check_order(order):
    """Returns an error message if the order is bad, otherwise None."""
    if len(order["items"]) == 0:
        return "order is empty"
    for name in order["items"]:
        if name not in menu:
            return "'" + name + "' is not on the menu"
        if order["items"][name] <= 0:
            return "invalid quantity for " + name
    return None


# process every order

valid_orders = []
invalid_orders = []

for order in orders:
    error = check_order(order)
    if error:
        print("Order", order["order_id"], "skipped:", error)
        invalid_orders.append({"order_id": order["order_id"], "reason": error})
        continue

    total = calculate_total(order["items"])
    discount = apply_discount(total)
    final_bill = add_delivery(total - discount)

    valid_orders.append({
        "order_id": order["order_id"],
        "customer": order["customer"],
        "total": total,
        "discount": discount,
        "final_bill": final_bill,
    })
    print("Order", order["order_id"], "-", order["customer"], "- bill: Rs", final_bill)


# Step 4: highest value order

highest = None
for order in valid_orders:
    if highest is None or order["final_bill"] > highest["final_bill"]:
        highest = order

if highest:
    print("\nHighest order: #" + str(highest["order_id"]), highest["customer"],
          "- Rs", highest["final_bill"])
else:
    print("\nNo valid orders to compare")


# Step 5: write the sales summary to a file

total_revenue = 0
for order in valid_orders:
    total_revenue = total_revenue + order["final_bill"]

with open("sales_report.txt", "w") as f:
    f.write("DAILY SALES SUMMARY\n")
    f.write("-------------------\n")
    f.write("Total orders received: " + str(len(orders)) + "\n")
    f.write("Valid orders: " + str(len(valid_orders)) + "\n")
    f.write("Invalid orders: " + str(len(invalid_orders)) + "\n")
    f.write("Total revenue: Rs " + str(total_revenue) + "\n")
    if highest:
        f.write("Highest value order: #" + str(highest["order_id"]) + " (" +
                highest["customer"] + ") - Rs " + str(highest["final_bill"]) + "\n")

    f.write("\nOrder bills\n")
    for order in valid_orders:
        f.write("Order " + str(order["order_id"]) + " | " + order["customer"] +
                " | total Rs " + str(order["total"]) +
                " | discount Rs " + str(order["discount"]) +
                " | final Rs " + str(order["final_bill"]) + "\n")

    if invalid_orders:
        f.write("\nInvalid orders\n")
        for order in invalid_orders:
            f.write("Order " + str(order["order_id"]) + ": " + order["reason"] + "\n")

# save the sample order data too
with open("sample_orders.json", "w") as f:
    json.dump(orders, f, indent=2)

print("Sales report saved to sales_report.txt")
