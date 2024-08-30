import requests

# Define the base URL of the API
base_url = "http://127.0.0.1:8000"

# Example: Call the API to get a single product by ID
def get_product(product_id):
    url = f"{base_url}/products/{product_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Product Details:", response.json())
    except requests.exceptions.HTTPError as err:
        print("Error:", err)

# Example: Call the API to get multiple products by IDs
def get_products(product_ids):
    url = f"{base_url}/products/"
    try:
        response = requests.get(url, params={'product_ids': product_ids})
        response.raise_for_status()
        print("Products Details:", response.json())
    except requests.exceptions.HTTPError as err:
        print("Error:", err)

# Test the API
if __name__ == "__main__":
    # Call to get a single product with ID 1
    get_product(1)

    # Call to get multiple products with IDs 1, 2, and 3
    get_products([1, 2, 3])
