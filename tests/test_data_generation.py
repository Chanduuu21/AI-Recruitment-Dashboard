import tempfile
import unittest
from pathlib import Path

import pandas as pd

from data_generation import Config, generate_datasets, validate_datasets, write_datasets


class DataGenerationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config(
            seed=7,
            candidates=25,
            jobs=6,
            applications=50,
            matches=20,
            users=4,
            system_metrics=10,
        )

    def test_expected_datasets_and_row_counts(self) -> None:
        datasets = generate_datasets(self.config)

        self.assertEqual(
            set(datasets),
            {
                "Candidates",
                "CandidateSkills",
                "Applications",
                "Jobs",
                "JobSkills",
                "Matches",
                "Users",
                "SystemMetrics",
            },
        )
        self.assertEqual(len(datasets["Candidates"]), 25)
        self.assertEqual(len(datasets["Jobs"]), 6)
        self.assertEqual(len(datasets["Applications"]), 50)
        self.assertEqual(len(datasets["Matches"]), 20)
        self.assertEqual(len(datasets["Users"]), 4)

    def test_generation_is_reproducible_for_same_seed(self) -> None:
        first = generate_datasets(self.config)
        second = generate_datasets(self.config)

        for name in first:
            pd.testing.assert_frame_equal(first[name], second[name])

    def test_foreign_keys_and_ranges_pass_validation(self) -> None:
        datasets = generate_datasets(self.config)
        validate_datasets(datasets)

        self.assertTrue(
            set(datasets["Applications"]["CandidateID"]).issubset(
                set(datasets["Candidates"]["CandidateID"])
            )
        )
        self.assertTrue(datasets["Matches"]["SimilarityScore"].between(0, 100).all())

    def test_writer_creates_eight_csv_files(self) -> None:
        datasets = generate_datasets(self.config)

        with tempfile.TemporaryDirectory() as directory:
            paths = write_datasets(datasets, Path(directory))

            self.assertEqual(len(paths), 8)
            self.assertTrue(all(path.exists() for path in paths))
            self.assertEqual(
                len(pd.read_csv(Path(directory) / "Applications.csv")),
                self.config.applications,
            )


if __name__ == "__main__":
    unittest.main()

