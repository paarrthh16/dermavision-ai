# src/database/load_products.py

import pandas as pd
# Import the class from your db_client.py file
from db_client import DatabaseClient

import os

def upload_products_from_csv():
    """Reads product data from a CSV and uploads it using your DatabaseClient."""
    
    # Establish a connection to the database
    db = DatabaseClient()
    if not db.use_supabase:
        print("⚠️ Running in SQLite fallback mode. Products will be loaded locally.")

    # Define the path to your products.csv file
    csv_path = os.path.join('data', 'products', 'products.csv')

    if not os.path.exists(csv_path):
        print(f"❌ Error: Product data file not found at {csv_path}")
        return

    print(f"Reading product data from {csv_path}...")
    products_df = pd.read_csv(csv_path)
    
    # Fill any missing values with a placeholder to avoid errors
    products_df.fillna('', inplace=True)
    
    products_to_upload = products_df.to_dict(orient='records')

    print(f"Found {len(products_to_upload)} products to upload.")

    # Loop through and insert each product
    for i, product in enumerate(products_to_upload):
        try:
            # Use the insert_product method from your DatabaseClient class
            db.insert_product(product)
            print(f"  ({i+1}/{len(products_to_upload)}) Successfully uploaded: {product.get('name')}")
        except Exception as e:
            print(f"  ({i+1}/{len(products_to_upload)}) ❌ Failed to upload {product.get('name')}: {e}")

    print("\n✅ Product upload process complete!")

if __name__ == "__main__":
    upload_products_from_csv()