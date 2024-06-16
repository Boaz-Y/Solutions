import pandas as pd
import argparse

def shorten_proteome(input_file, output_file, proportion):
    # Read the input CSV file
    df = pd.read_csv(input_file)

    # Calculate the number of rows to keep based on the given proportion
    num_rows_to_keep = int(len(df) * proportion)

    # Randomly select rows to keep
    df_sampled = df.sample(n=num_rows_to_keep, random_state=1)

    # Save the sampled rows to the output CSV file
    df_sampled.to_csv(output_file, index=False)

    print(f"Successfully kept {proportion * 100}% of lines. The result is saved in '{output_file}'.")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Reduce the size of a proteome CSV file by keeping a specified proportion of rows.")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("output_file", help="Path to the output CSV file")
    parser.add_argument("proportion", type=float, help="Proportion of rows to keep (between 0 and 1)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    shorten_proteome(args.input_file, args.output_file, args.proportion)
