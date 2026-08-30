"""
Reservoir Sampling Algorithm Implementation

This module implements the Reservoir Sampling algorithm to maintain a random
sample of k elements from a stream of unknown size.

Usage:
    python ReservoirSampling.py <k> <input_file> [-v|--verbose]
    
Example:
    python ReservoirSampling.py 5 data.txt
    python ReservoirSampling.py 5 data.txt --verbose
"""

import random
import sys
from pathlib import Path
from typing import List, Optional


def print_sample_table(sample: List[Optional[str]]) -> None:
    """
    Display the current sample contents in a formatted table.

    Args:
        sample: List containing the current sample elements

    Returns:
        None
    """
    print("+--------+----------------+")
    print("|   #    |     Line       |")
    print("+--------+----------------+")
    for i, element in enumerate(sample, 1):
        element_str = str(element).strip() if element else "None"
        print(f"|   {i}    | {element_str:<14} |")
    print("+--------+----------------+")


def validate_arguments(args: list) -> tuple[int, str, bool]:

    if len(args) < 2:
        print("Error: Missing required arguments")
        print(__doc__)
        sys.exit(1)

    verbose = "-v" in args or "--verbose" in args

    positional_args = [
        arg for arg in args
        if arg not in ("-v", "--verbose")
    ]

    if len(positional_args) < 2:
        print("Error: Missing required arguments")
        print(__doc__)
        sys.exit(1)

    try:
        k = int(positional_args[0])

        if k <= 0:
            print("Error: k must be a positive integer")
            sys.exit(1)

    except ValueError:
        print(f"Error: k must be an integer, got '{positional_args[0]}'")
        sys.exit(1)

    input_file_path = positional_args[1]

    if not Path(input_file_path).is_file():
        print(f"Error: File '{input_file_path}' not found")
        sys.exit(1)

    return k, input_file_path, verbose


def reservoir_sample(k: int, input_file_path: str, verbose: bool = False) -> List[str]:
    """
    Execute the reservoir sampling algorithm on a file stream.

    Args:
        k: Size of the reservoir sample
        input_file_path: Path to input file
        verbose: If True, print detailed processing information

    Returns:
        List of sampled elements
    """
    sample: List[Optional[str]] = [None] * k
    stream_index = 0

    if verbose:
        print(f"Starting reservoir sampling with k={k}")
        print(f"Input file: {input_file_path}\n")
        print_sample_table(sample)

    with open(input_file_path) as file:
        for line in file:
            line = line.strip()

            if not line:
                continue  # Skip empty lines

            stream_index += 1

            if verbose:
                print(f"\nIncoming element #{stream_index}: {line}")

            if stream_index <= k:
                # Fill reservoir with first k elements
                sample[stream_index - 1] = line
                if verbose:
                    print("-> Added to reservoir")
                    print_sample_table(sample)
            else:
                # Use probability to decide whether to include element
                probability_threshold = k / stream_index
                random_probability = random.random()

                if verbose:
                    print(f"  Probability threshold (k/n): {probability_threshold:.4f}")
                    print(f"  Random probability: {random_probability:.4f}")

                if random_probability > probability_threshold:
                    if verbose:
                        print("-> Element rejected (random probability > threshold)")
                        print_sample_table(sample)
                else:
                    replacement_index = random.randint(0, k - 1)
                    sample[replacement_index] = line
                    if verbose:
                        print(f"-> Element accepted, replacing index {replacement_index}")
                        print_sample_table(sample)

    return [elem for elem in sample if elem is not None]


def main() -> None:
    """
    Execute the reservoir sampling program.

    Reads command-line arguments, validates them, and runs the reservoir
    sampling algorithm on the input file. Prints the final sample to stdout.
    """
    k, input_file_path, verbose = validate_arguments(sys.argv[1:])
    sample = reservoir_sample(k, input_file_path, verbose)

    print("\n" + "=" * 40)
    print("FINAL SAMPLE")
    print("=" * 40)
    for i, element in enumerate(sample, 1):
        print(f"{i}. {element}")
    print("=" * 40)


if __name__ == "__main__":
    main()