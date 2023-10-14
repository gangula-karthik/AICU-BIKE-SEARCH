from carousell_scraping_functions import *
import pandas as pd
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor


# Main execution
url = "https://www.carousell.sg/categories/sports-equipment-10/bicycles-parts-1900/bicycles-247?addRecent=false&canChangeKeyword=false&includeSuggestions=false&sc=0a0208301a0408bbe172220c0a0862696379636c657378012a110a095f64656c69766572793a02080078012a160a0b636f6c6c656374696f6e7312050a0332343778013204080378013a02180742060801100118004a08200128014001480150005a020801&search=bicycles&searchId=6Oyxkt&sort_by=3&tab=marketplace"


driver = initialize_driver(url)
scroll_page(driver, max_scrolls=1)
productList = extract_product_data(driver)

print(productList)

df = pd.DataFrame(productList)
df.to_csv('test.csv', index=False)

status = close_driver(driver)
print(status)

CHUNK_SIZE = 10
df = pd.read_csv("test.csv")

if 'condition' not in df.columns:
    df['condition'] = None
if 'description' not in df.columns:
    df['description'] = None

def process_chunk(chunk):
    with webdriver.Chrome() as driver:  # Open a new WebDriver instance for each chunk
        for idx, row in chunk.iterrows():
            try:
                condition, description = extract_condition_and_description(driver, row['listing_link'])
                df.at[idx, 'condition'] = condition
                df.at[idx, 'description'] = description
            except Exception as e:
                print(f"Error processing link at index {idx}: {e}")

# Divide the DataFrame into chunks and process them concurrently
with ThreadPoolExecutor() as executor:
    chunks = [df.iloc[i:i+CHUNK_SIZE] for i in range(0, len(df), CHUNK_SIZE)]
    executor.map(process_chunk, chunks)

# Save the updated data to a new CSV file
df.to_csv('test_updated.csv', index=False)