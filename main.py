import argparse
from data.data_collector import traverse_folder

def main():
    parser = argparse.ArgumentParser(description="deep-riscv-formal data collector")
    parser.add_argument("folder", help="the name of the folder that contains the data")
    args = parser.parse_args()
    folder = args.folder
    performance_data = traverse_folder(folder)
    for data in performance_data:
        print(data)


if __name__ == '__main__':
    main()
