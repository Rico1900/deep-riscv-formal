import os
from pathlib import Path
from data.logfile_parser import clock_time_summary, EnginePerformance
from parsy import ParseError
from dataclasses import dataclass
from checks.constant import TIMEOUT
from functools import reduce


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

    def champion(self) -> Item:
        return min(self.statistics, key=lambda i: i.time_consumption)

    def __str__(self):
        details = reduce(lambda u, d: u + "\n" + d,
                         map(lambda i: f"\t{str(i)}", self.statistics))
        return f"Task Name: {self.task_name}\n{details}"


@dataclass
class Statistics:
    summary: dict[str, int]
    details: list[Group]

    def __str__(self):
        summary = reduce(lambda acc, s: f"{acc}\tconfig={s[0]}, count={s[1]}\n", self.summary.items(), "")
        groups = reduce(lambda acc, g: f"{acc}\n\n{g}", self.details, "")
        return f"Summary:\n{summary}{groups}"


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


def generate_statistics(data: list[EnginePerformance]) -> Statistics:
    groups = dict()
    for log in data:
        if log.task_name not in groups:
            groups[log.task_name] = []
        groups[log.task_name].append(Item(checking_config=log.checking_config, time_consumption=log.time_consumption))
    summary = dict()
    detail = []
    for k, v in groups.items():
        v.sort(key=lambda i: i.checking_config)
        group = Group(task_name=k, statistics=v)
        champion = group.champion()
        if champion.checking_config not in summary:
            summary[champion.checking_config] = 1
        else:
            summary[champion.checking_config] += 1
        detail.append(group)
    return Statistics(summary=summary, details=detail)


def statistics(directory: str) -> Statistics:
    return generate_statistics(traverse_folder(directory))
