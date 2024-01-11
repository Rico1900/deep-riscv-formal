import os
from pathlib import Path
from data.logfile_parser import clock_time_summary, EnginePerformance
from parsy import ParseError
from dataclasses import dataclass
from checks.constant import TIMEOUT
from functools import reduce
from itertools import groupby


@dataclass
class Item:
    checking_config: str
    time_consumption: int

    def __str__(self):
        return f"config={self.checking_config}, time={self.time_consumption}"


@dataclass
class Group:
    task_name: str
    statistics: list[Item]

    def __str__(self):
        details = reduce(lambda u, d: u + "\n" + d,
                         map(lambda i: f"\t{str(i)}", self.statistics))
        return f"task name: {self.task_name}\n{details}"


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


def sort_statistics(data: list[EnginePerformance]) -> list[Group]:
    groups = dict()
    for log in data:
        if log.task_name not in groups:
            groups[log.task_name] = []
        groups[log.task_name].append(Item(checking_config=log.checking_config, time_consumption=log.time_consumption))
    result = []
    for k, v in groups.items():
        v.sort(key=lambda i: i.checking_config)
        result.append(Group(task_name=k, statistics=v))
    return result
