import pandas as pd
import time


def clean_chunk(df):
    df = df.copy()
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
    df = df.replace("", pd.NA)
    df = df.dropna(how='all')
    return df


def process_large_file(path_in, path_out, chunksize=50000):
    start_time = time.time()
    total_rows_in = 0
    total_rows_out = 0
    first_write = True

    for chunk in pd.read_csv(path_in, chunksize=chunksize):
        total_rows_in += len(chunk)
        cleaned = clean_chunk(chunk)
        total_rows_out += len(cleaned)

        cleaned.to_csv(
            path_out,
            mode='w' if first_write else 'a',
            header=first_write,
            index=False
        )
        first_write = False

    elapsed = time.time() - start_time
    print("=== Processing Summary ===")
    print(f"Input rows: {total_rows_in}")
    print(f"Output rows after cleaning: {total_rows_out}")
    print(f"Rows removed: {total_rows_in - total_rows_out}")
    print(f"Time taken: {elapsed:.2f} seconds")


if __name__ == '__main__':
    input_file = 'day13_large_users.csv'
    output_file = 'day13_cleaned_users.csv'
    chunk_size = 50000

    print("Processing large dataset...")
    process_large_file(input_file, output_file, chunksize=chunk_size)