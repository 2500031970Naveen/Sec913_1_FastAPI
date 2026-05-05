products = [
    {"name": "laptop", "price": 1000},
    {"name": "phone", "price": 500},
    {"name": "tablet", "price": 300}
]

# Convert input to integers
min_price = int(input("Enter minimum price: "))
max_price = int(input("Enter maximum price: "))

# Filter products
filtered_products = [p for p in products if min_price <= p["price"] <= max_price]

# Sort filtered products
sorted_products = sorted(filtered_products, key=lambda x: x["price"])

# Display output
for p in sorted_products:
    print(p["name"], "-", p["price"])