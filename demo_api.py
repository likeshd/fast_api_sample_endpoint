import requests

# Define the base URL of the API
base_url = "http://127.0.0.1:8000"

# Example: Call the API to get a single product by ID
def get_product(product_id):
    url = f"{base_url}/products/{product_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Product Details:", response.json())
    else:
        print("Error:", response.status_code, response.json())

# Example: Call the API to get multiple products by IDs
def get_products(product_ids):
    url = f"{base_url}/products/"
    response = requests.get(url, params={'product_ids': product_ids})
    
    if response.status_code == 200:
        print("Products Details:", response.json())
    else:
        print("Error:", response.status_code, response.json())

# Test the API
if __name__ == "__main__":
    # Call to get a single product with ID 1
    get_product(1)

    # Call to get multiple products with IDs 1, 2, and 3
    get_products([1, 2, 3])
