import pandas as pd

input_file = 'proteome.csv' 
output_file = 'shortened_proteome.csv' 

df = pd.read_csv(input_file)

num_rows_to_keep = int(len(df) * 0.45)

# Randomly select rows to keep
df_sampled = df.sample(n=num_rows_to_keep, random_state=1)

df_sampled.to_csv(output_file, index=False)

print(f"Successfully deleted 55% of lines. The result is saved in '{output_file}'.")
