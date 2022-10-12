import glob
import os.path
from typing import Iterator, Optional

import yaml
from yaml import FullLoader

import atomic_red_team.pattern_matching
from atomic_red_team.constants import DEFAULT_ATOMIC_RED_TEAM_DIR

import logging

from atomic_red_team.types import STRS

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, atomic_red_team_dir: str = DEFAULT_ATOMIC_RED_TEAM_DIR):
        if not os.path.exists(atomic_red_team_dir):
            raise FileNotFoundError(atomic_red_team_dir)
        elif not os.path.isdir(atomic_red_team_dir):
            raise NotADirectoryError(atomic_red_team_dir)

        self.atomic_red_team_dir = atomic_red_team_dir

    def count_tests(
            self,
            test_ids: Optional[STRS] = None,
            test_names: Optional[STRS] = None,
            technique_ids: Optional[STRS] = None) -> int:

        tests = self.iter_tests(test_ids=test_ids, test_names=test_names, technique_ids=technique_ids)
        return sum(1 for _ in tests)

    def iter_tests(
            self,
            test_ids: Optional[STRS] = None,
            test_names: Optional[STRS] = None,
            technique_ids: Optional[STRS] = None) -> Iterator[dict]:

        test_ids = set(test_ids) if test_ids else None
        test_names = set(test_names) if test_names else None
        technique_ids = set(technique_ids) if technique_ids else None

        for path in self.iter_test_paths():
            if technique_ids:
                technique_id = os.path.basename(path).removesuffix('.yaml')
                if not atomic_red_team.pattern_matching.matches(technique_id, technique_ids):
                    continue

            for test in self.read_tests_from_file(path):
                if test_ids and test['auto_generated_guid'] not in test_ids:
                    continue

                if test_names and not atomic_red_team.pattern_matching.matches(test['name'], test_names):
                    continue

                yield test

    def iter_test_paths(self, technique_ids: Optional[STRS] = None) -> Iterator[str]:
        for path in glob.glob(os.path.join(self.atomic_red_team_dir, "atomics/T*/T*.yaml")):
            if technique_ids:
                technique_id = os.path.basename(path).split('.yaml')[0]
                if technique_id not in technique_ids:
                    continue

            yield path

    def read_tests_from_file(self, path: str) -> Iterator[dict]:
        with open(path) as file:
            data = yaml.load(file, Loader=FullLoader)
            yield from data['atomic_tests']

    def get_test(self, test_id: str, technique_id: Optional[str] = None) -> Optional[dict]:
        technique_ids = [technique_id] if technique_id else None
        tests = self.iter_tests(test_ids=[test_id], technique_ids=technique_ids)
        return next(tests, None)
