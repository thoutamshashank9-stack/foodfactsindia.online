import pandas as pd

# Load extracted product additives
df = pd.read_csv('product_additives.csv')

# Calculate frequency of each unique additive code
unique_codes = df['additive_code'].value_counts().reset_index()
unique_codes.columns = ['additive_code', 'product_count']

# Save to CSV for Phase 2 regulatory rulebook mapping
unique_codes.to_csv('unique_additives_to_research.csv', index=False)

print(f"Total unique additive codes in dataset: {len(unique_codes)}")
print("\nTop 30 Most Frequent Additive Codes in India OFF Dataset:")
print(unique_codes.head(30).to_string(index=False))
