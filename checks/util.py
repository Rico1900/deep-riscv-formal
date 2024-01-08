from typing import List

def none_str(s: str) -> str:
    return "" if s is None else s

def not_none(s: str) -> bool:
    return (s is not None) and (s != "")

def process_single_engine_cfg(option: str) -> str:
    if option.startswith("--"):
        return option[2:]
    elif option.startswith("-"):
        return option[1:]
    else:
        return option
def process_engine_cfg(cfg: str) -> str:
    if cfg is None:
        return ""
    options: List[str] = list(
        map(process_single_engine_cfg,
            filter(not_none, cfg.split(" ")))
    )
    return "_".join(options)
