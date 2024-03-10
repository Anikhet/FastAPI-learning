import requests

base_url = "http://127.0.0.1:8000"

# First round: Place an order (this will be rejected)
order_data = {
    "product_id": "P003",
    "quantity": 2,
    "account": "A002"
}
headers = {"Username": "user", "Password": "pass"}
response = requests.post(f"{base_url}/orders/", json=order_data, headers=headers)
print("First round (Order placement):")
print(f"Status Code: {response.status_code}")
print(response.json())

# Second round: Perform a query, then place an order
# Query the product
product_id = "P003"
response = requests.get(f"{base_url}/products/{product_id}")
print("\nSecond round (Query):")

print(response.json())
print()

# Place the order using the queried product
response = requests.post(f"{base_url}/orders/", json=order_data, headers=headers)
print("Third round (Order placement):")
print(f"Status Code: {response.status_code}")
print(response.json())
