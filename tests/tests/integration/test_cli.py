import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = PROJECT_ROOT / "reservoir_sampling.py"


def create_input_file(tmp_path: Path, lines: list[str]) -> Path:
    """Create a temporary input file with the provided lines."""
    input_file = tmp_path / "input.txt"
    input_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return input_file


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the reservoir sampling CLI."""
    return subprocess.run(
        [sys.executable, str(SCRIPT_PATH), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class TestCLI:
    """Integration tests for the command-line interface."""

    def test_runs_successfully(
        self,
        tmp_path: Path,
    ) -> None:
        input_file = create_input_file(
            tmp_path,
            [f"item-{i}" for i in range(20)],
        )

        result = run_cli("5", str(input_file))

        assert result.returncode == 0
        assert "FINAL SAMPLE" in result.stdout
        assert result.stderr == ""

    def test_outputs_correct_number_of_elements(
        self,
        tmp_path: Path,
    ) -> None:
        input_file = create_input_file(
            tmp_path,
            [f"item-{i}" for i in range(20)],
        )

        result = run_cli("5", str(input_file))

        assert result.returncode == 0

        sample_lines = [
            line
            for line in result.stdout.splitlines()
            if line.startswith(tuple(f"{i}." for i in range(1, 6)))
        ]

        assert len(sample_lines) == 5

    def test_verbose_mode(
        self,
        tmp_path: Path,
    ) -> None:
        input_file = create_input_file(
            tmp_path,
            ["alpha", "beta", "gamma"],
        )

        result = run_cli("2", str(input_file), "--verbose")

        assert result.returncode == 0
        assert "Starting reservoir sampling with k=2" in result.stdout
        assert "Incoming element #1: alpha" in result.stdout
        assert "FINAL SAMPLE" in result.stdout

    def test_short_verbose_flag(
        self,
        tmp_path: Path,
    ) -> None:
        input_file = create_input_file(
            tmp_path,
            ["alpha", "beta"],
        )

        result = run_cli("1", str(input_file), "-v")

        assert result.returncode == 0
        assert "Starting reservoir sampling" in result.stdout

    def test_rejects_missing_arguments(self) -> None:
        result = run_cli()

        assert result.returncode == 1
        assert "Missing required arguments" in result.stdout

    def test_rejects_invalid_k(
        self,
        tmp_path: Path,
    ) -> None:
        input_file = create_input_file(tmp_path, ["alpha"])

        result = run_cli("0", str(input_file))

        assert result.returncode == 1
        assert "k must be a positive integer" in result.stdout

    def test_rejects_non_integer_k(
        self,
        tmp_path: Path,
    ) -> None:
        input_file = create_input_file(tmp_path, ["alpha"])

        result = run_cli("abc", str(input_file))

        assert result.returncode == 1
        assert "k must be an integer" in result.stdout

    def test_rejects_missing_input_file(self) -> None:
        result = run_cli("5", "does-not-exist.txt")

        assert result.returncode == 1
        assert "not found" in result.stdout

    def test_k_larger_than_input(
        self,
        tmp_path: Path,
    ) -> None:
        input_file = create_input_file(
            tmp_path,
            ["alpha", "beta", "gamma"],
        )

        result = run_cli("10", str(input_file))

        assert result.returncode == 0
        assert "1. alpha" in result.stdout
        assert "2. beta" in result.stdout
        assert "3. gamma" in result.stdout