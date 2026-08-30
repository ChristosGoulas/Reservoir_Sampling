import random
from pathlib import Path

import pytest

from reservoir_sampling import (
    print_sample_table,
    reservoir_sample,
    validate_arguments,
)


def create_input_file(tmp_path: Path, lines: list[str]) -> Path:
    """Create a temporary input file with the provided lines."""
    input_file = tmp_path / "input.txt"
    input_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return input_file


class TestReservoirSample:
    """Unit tests for the reservoir sampling algorithm."""

    def test_returns_k_elements_when_stream_is_larger_than_k(
        self,
        tmp_path: Path,
    ) -> None:
        lines = [f"item-{i}" for i in range(100)]
        input_file = create_input_file(tmp_path, lines)

        random.seed(42)
        sample = reservoir_sample(10, str(input_file))

        assert len(sample) == 10
        assert len(set(sample)) == 10
        assert all(element in lines for element in sample)

    def test_returns_all_elements_when_k_equals_stream_size(
        self,
        tmp_path: Path,
    ) -> None:
        lines = ["a", "b", "c", "d", "e"]
        input_file = create_input_file(tmp_path, lines)

        sample = reservoir_sample(5, str(input_file))

        assert sample == lines

    def test_returns_all_elements_when_k_is_larger_than_stream(
        self,
        tmp_path: Path,
    ) -> None:
        lines = ["a", "b", "c"]
        input_file = create_input_file(tmp_path, lines)

        sample = reservoir_sample(10, str(input_file))

        assert sample == lines

    def test_empty_file_returns_empty_sample(
        self,
        tmp_path: Path,
    ) -> None:
        input_file = create_input_file(tmp_path, [])

        sample = reservoir_sample(5, str(input_file))

        assert sample == []

    def test_sample_contains_only_input_elements(
        self,
        tmp_path: Path,
    ) -> None:
        lines = ["alpha", "beta", "gamma", "delta"]
        input_file = create_input_file(tmp_path, lines)

        random.seed(123)
        sample = reservoir_sample(2, str(input_file))

        assert len(sample) == 2
        assert set(sample).issubset(set(lines))

    def test_random_replacement_can_occur(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        lines = ["a", "b", "c"]
        input_file = create_input_file(tmp_path, lines)

        # Force the third element to be accepted and replace index 0.
        random_values = iter([0.0])

        monkeypatch.setattr(
            random,
            "random",
            lambda: next(random_values),
        )
        monkeypatch.setattr(
            random,
            "randint",
            lambda _start, _end: 0,
        )

        sample = reservoir_sample(2, str(input_file))

        assert sample == ["c", "b"]

    def test_random_rejection_can_occur(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        lines = ["a", "b", "c"]
        input_file = create_input_file(tmp_path, lines)

        # At n=3 and k=2, probability threshold is 2/3.
        # Force random.random() above that threshold.
        monkeypatch.setattr(random, "random", lambda: 0.99)

        sample = reservoir_sample(2, str(input_file))

        assert sample == ["a", "b"]

    def test_verbose_mode_prints_processing_information(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        lines = ["a", "b"]
        input_file = create_input_file(tmp_path, lines)

        reservoir_sample(2, str(input_file), verbose=True)

        output = capsys.readouterr().out

        assert "Starting reservoir sampling with k=2" in output
        assert f"Input file: {input_file}" in output
        assert "Incoming element #1: a" in output
        assert "Incoming element #2: b" in output


class TestValidateArguments:
    """Unit tests for command-line argument validation."""

    def test_accepts_valid_arguments(
        self,
        tmp_path: Path,
    ) -> None:
        input_file = create_input_file(tmp_path, ["a", "b"])

        result = validate_arguments(["2", str(input_file)])

        assert result == (2, str(input_file), False)

    @pytest.mark.parametrize("flag", ["-v", "--verbose"])
    def test_accepts_verbose_flags(
        self,
        tmp_path: Path,
        flag: str,
    ) -> None:
        input_file = create_input_file(tmp_path, ["a", "b"])

        result = validate_arguments(["2", str(input_file), flag])

        assert result == (2, str(input_file), True)

    def test_accepts_verbose_flag_in_any_position(
        self,
        tmp_path: Path,
    ) -> None:
        input_file = create_input_file(tmp_path, ["a", "b"])

        result = validate_arguments(
            ["2", "--verbose", str(input_file)],
        )

        assert result == (2, str(input_file), True)

    def test_rejects_missing_arguments(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        with pytest.raises(SystemExit) as exc:
            validate_arguments([])

        assert exc.value.code == 1
        assert "Missing required arguments" in capsys.readouterr().out

    @pytest.mark.parametrize("value", ["0", "-1", "-100"])
    def test_rejects_non_positive_k(
        self,
        tmp_path: Path,
        value: str,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        input_file = create_input_file(tmp_path, ["a"])

        with pytest.raises(SystemExit) as exc:
            validate_arguments([value, str(input_file)])

        assert exc.value.code == 1
        assert "k must be a positive integer" in capsys.readouterr().out

    def test_rejects_non_integer_k(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        input_file = create_input_file(tmp_path, ["a"])

        with pytest.raises(SystemExit) as exc:
            validate_arguments(["abc", str(input_file)])

        assert exc.value.code == 1
        assert "k must be an integer" in capsys.readouterr().out

    def test_rejects_missing_file(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        with pytest.raises(SystemExit) as exc:
            validate_arguments(["5", "does-not-exist.txt"])

        assert exc.value.code == 1
        assert "not found" in capsys.readouterr().out


class TestPrintSampleTable:
    """Unit tests for sample table formatting."""

    def test_prints_sample_table(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        print_sample_table(["alpha", "beta"])

        output = capsys.readouterr().out

        assert "Line" in output
        assert "alpha" in output
        assert "beta" in output

    def test_prints_none_for_empty_slots(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        print_sample_table([None, "alpha"])

        output = capsys.readouterr().out

        assert "None" in output
        assert "alpha" in output