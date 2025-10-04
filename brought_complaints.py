import argparse
import os
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Process some NYC complaints.")
    parser.add_argument(
        "-i", type=str, required=True, help="Input csv file", metavar="input_file"
    )
    parser.add_argument(
        "-s", type=str, required=True, help="Start date", metavar="start_date"
    )
    parser.add_argument(
        "-e", type=str, required=True, help="End date", metavar="end_date"
    )
    parser.add_argument(
        "-o",
        type=str,
        required=False,
        help="Output file",
        metavar="output_file",
        default=None,
    )

    args = parser.parse_args()

    chunk_list = []
    for chunk in pd.read_csv(args.i, chunksize=100000, low_memory=False):
        chunk["Created Date"] = pd.to_datetime(chunk["Created Date"])
        filtered_chunk = chunk[
            (chunk["Created Date"] >= pd.to_datetime(args.s))
            & (chunk["Created Date"] <= pd.to_datetime(args.e))
        ]
        chunk_list.append(filtered_chunk)

    df = pd.concat(chunk_list, ignore_index=True)

    if args.o is not None:
        df.to_csv(args.o, index=False)

    else:
        print(df)


if __name__ == "__main__":
    main()
