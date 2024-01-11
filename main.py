import argparse
from data.data_collector import statistics


def main():
    parser = argparse.ArgumentParser(description="deep-riscv-formal data collector")
    parser.add_argument("folder", help="the name of the folder that contains the data")
    args = parser.parse_args()
    folder = args.folder
    data = statistics(folder)
    print(data)


if __name__ == '__main__':
    main()
