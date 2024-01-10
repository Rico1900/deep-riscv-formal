import argparse
import os
from pathlib import Path
from logfile_parser import clock_time_summary, EnginePerformance
from parsy import ParseError
from config.constant import TIMEOUT


def traverse_folder(directory: str):
    result = []
    file_names = os.listdir(directory)
    for name in file_names:
        file_path = Path(os.path.join(directory, name))
        if file_path.is_dir():
            log_file_path = file_path.joinpath(Path("logfile.txt"))
            with log_file_path.open("r") as log_file:
                content = log_file.read()
                not_found = True
                for line in content.split("\n"):
                    try:
                        data = clock_time_summary.parse(line)
                        result.append(data)
                        not_found = False
                        break
                    except ParseError:
                        continue
                if not_found:
                    result.append(EnginePerformance(name=name, time_consumption=TIMEOUT))
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
