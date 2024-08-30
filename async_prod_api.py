import asyncio
import httpx

# Define the base URL of the API
base_url = "http://127.0.0.1:8000"

# Example: Asynchronously call the API to get a single product by ID
async def get_product(product_id):
    url = f"{base_url}/products/{product_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        print("Product Details:", response.json())

# Example: Asynchronously call the API to get multiple products by IDs
async def get_products(product_ids):
    url = f"{base_url}/products/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={'product_ids': product_ids})
        response.raise_for_status()
        print("Products Details:", response.json())

# Run the asynchronous tasks
async def main():
    # Call to get a single product with ID 1
    await get_product(1)

    # Call to get multiple products with IDs 1, 2, and 3
    await get_products([1, 2, 3])

if __name__ == "__main__":
    asyncio.run(main())
