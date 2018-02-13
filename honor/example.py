#!/usr/bin/env python3

import datasets
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", choices=["cornell", "opensubs"], help="Name of the dataset.")
    parser.add_argument("--max_len", type=int, default=10, help="Max length of sentences to consider.")
    args = parser.parse_args()

    dataset_path = os.path.join("data", args.dataset)
    if args.dataset == "cornell":
        data = datasets.readCornellData(dataset_path, max_len=args.max_len)
    elif args.dataset == "opensubs":
        data = datasets.readOpensubsData(dataset_path, max_len=args.max_len)
    else:
        raise ValueError("Unrecognized dataset: {!r}".format(args.dataset))

    print("Size of dataset: {}".format(len(data)))
    print("First 10 training pairs:")
    for item in data[:10]:
        print(item)

if __name__ == "__main__":
    main()
