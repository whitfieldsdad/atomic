import fnmatch
import glob
from typing import Union

from atomic_red_team.types import STRS
import atomic_red_team.types


def matches(values: Union[str, STRS], patterns: Union[str, STRS] = None) -> bool:
    values = atomic_red_team.types.to_lowercase_strings(values)
    patterns = atomic_red_team.types.to_lowercase_strings(patterns)

    for value in values:
        for pattern in patterns:
            if value == pattern or (glob.has_magic(pattern) and fnmatch.fnmatch(value, pattern)):
                return True
    return False
