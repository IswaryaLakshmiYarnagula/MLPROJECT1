import pandas as pd
import random
import re

# Load the input CSV file
input_file = "mlp1.csv"
df = pd.read_csv(input_file)

# Function to extract roll number from the text column
def extract_roll_number(text):
    match = re.search(r'\d{5}[A-Za-z0-9]+', text)
    return match.group(0) if match else None

# Extract roll numbers
if 'text' in df.columns:
    roll_numbers = df['text'].dropna().apply(extract_roll_number).dropna().unique().tolist()
else:
    raise ValueError("The input CSV does not have a 'text' column.")

# Ensure no repetition and add random roll numbers
existing_count = len(roll_numbers)
total_required = 150

# Generate random roll numbers for the remaining count
def generate_random_roll():
    return f"{random.randint(22550, 22559)}{random.choice('ABCDE')}" \
           f"{random.randint(1000, 9999)}"

while len(roll_numbers) < total_required:
    new_roll = generate_random_roll()
    if new_roll not in roll_numbers:
        roll_numbers.append(new_roll)

# Save the extracted roll numbers to a new CSV file
output_file = "cleaned_roll_numbers.csv"
pd.DataFrame(roll_numbers, columns=["Roll Number"]).to_csv(output_file, index=False)

print(f"Extracted roll numbers saved to: {output_file}")