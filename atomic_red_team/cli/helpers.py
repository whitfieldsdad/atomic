from typing import Optional, List


def str_to_strs(data: Optional[str]) -> List[str]:
    if not data:
        return []
    return data.split(',')


def str_to_ints(data: Optional[str]) -> List[int]:
    return [int(v) for v in str_to_strs(data)]
