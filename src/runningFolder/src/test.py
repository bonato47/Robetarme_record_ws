
import pandas as pd
import os

# Sample data for the DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 28, 22],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}

# Create a pandas DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print("DataFrame:")
print(df)

# Save the DataFrame to a CSV file
csv_filename = '../output_data.csv'
df.to_csv(csv_filename, index=False)

current_path = os.getcwd()
print(f"Current working directory: {current_path}")

