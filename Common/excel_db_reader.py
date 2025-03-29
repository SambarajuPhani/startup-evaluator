import pandas as pd

# Replace 'your_file.xlsx' with the path to your Excel file
df = pd.read_excel('sample_data.xlsx')

# Replace NaN or empty strings with 'Data not available'
df = df.fillna("Data not available")
df = df.replace(r'^\s*$', "Data not available", regex=True)

# Create formatted text for each row
text_chunks = []
for _, row in df.iterrows():
    row_text = "\n".join(f"{col}: {row[col]}" for col in df.columns)
    text_chunks.append(row_text)

# Combine all rows into one big chunk
final_text = "\n\n".join(text_chunks)

# Print or use the final text
print(final_text)