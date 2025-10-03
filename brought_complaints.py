import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Process some NYC complaints.")
    parser.add_argument("-i", type=str, required=True, help="Input csv file", metavar="input_file")
    parser.add_argument("-s", type=str, required=True, help="Start date", metavar="start_date")
    parser.add_argument("-e", type=str, required=True, help="End date", metavar="end_date")
    parser.add_argument("-o", type=str, required=False, help="Output file", metavar="output_file", default=None)

    args = parser.parse_args()

    df = pd.read_csv(args.i, low_memory=False)
    df["Created Date"] = pd.to_datetime(df["Created Date"])
    df = df[(df['Created Date'] >= pd.to_datetime(args.s)) & (df['Created Date'] <= pd.to_datetime(args.e))]

    if args.o is not None:
        df.to_csv(args.o, index=False)
    else:
        print(df)

if __name__ == "__main__":
    main()