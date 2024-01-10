import argparse
import os
from pathlib import Path
from data.logfile_parser import clock_time_summary
from parsy import ParseError


def traverse_folder(directory: str):
    result = []
    file_names = os.listdir(directory)
    for name in file_names:
        file_path = Path(os.path.join(directory, name))
        if file_path.is_dir():
            log_file_path = file_path.joinpath(Path("logfile.txt"))
            with log_file_path.open("r") as log_file:
                content = log_file.read()
                for line in content.split("\n"):
                    try:
                        data = clock_time_summary.parse(line)
                        result.append(data)
                    except ParseError:
                        continue
                print(f"{log_file_path} does not contains clock time summary")
    return result


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
