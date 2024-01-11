import argparse
from data.data_collector import traverse_folder, sort_statistics


def main():
    parser = argparse.ArgumentParser(description="deep-riscv-formal data collector")
    parser.add_argument("folder", help="the name of the folder that contains the data")
    args = parser.parse_args()
    folder = args.folder
    statistics = sort_statistics(traverse_folder(folder))
    for data in statistics:
        print(data)
        print()


if __name__ == '__main__':
    main()
