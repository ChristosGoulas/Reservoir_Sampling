# Reservoir Sampling

A professional Python implementation of the **Reservoir Sampling** algorithm. A randomized streaming algorithm that selects a uniform random sample of K elements from a data stream without storing the entire stream in memory.

**Key Features:**
- ✨ Memory-efficient: O(K) space complexity regardless of stream size
- 🎯 Mathematically proven: Guarantees uniform sampling probability
- 🔄 Single-pass: Processes stream sequentially, one element at a time
- 📊 Type-safe: Full Python type hints for production-grade code
- 🛡️ Robust: Input validation and error handling
- 📖 Well-documented: Comprehensive docstrings and examples

---

## Problem Statement

When processing massive data streams (e.g., logs, sensor data, network traffic), we often need to select a representative random sample without knowing the stream size in advance. Storing all elements in memory is impractical for large streams.

**Reservoir Sampling** solves this elegantly:
- Process stream **only once**
- Maintain exactly **K elements** in memory
- Achieve **uniform random distribution** across all elements

---

## Algorithm Overview

After processing N elements, every element has an equal probability of being in the reservoir:

$$P(\text{element in reservoir}) = \frac{K}{N}$$

### Algorithm Steps

Let:
- `K` = desired sample size
- `N` = number of elements processed so far

#### Phase 1: Fill the Reservoir
The first K elements are added directly to the reservoir.

$$P(\text{element in reservoir}) = 1 = \frac{K}{K}$$

#### Phase 2: Stream Processing
For each element at position N > K:

1. Accept the element with probability $\frac{K}{N}$
2. If accepted, replace a random existing element uniformly at random
3. If rejected, discard the element

### Pseudocode

```text
reservoir = [first K elements]

for each element x at position N > K:
    r = random value in [0, 1]
    
    if r ≤ K/N:
        i = random index in [0, K-1]
        reservoir[i] = x
    
    // otherwise discard x

return reservoir
```

### Complexity Analysis

| Metric | Complexity | Notes |
|--------|-----------|-------|
| **Time** | O(N) | Single pass through stream |
| **Space** | O(K) | Fixed reservoir size |
| **Sample Quality** | Uniform | Every element has P = K/N |

---

## Installation & Usage

### Requirements
- Python 3.7+

### Basic Usage

```bash
python3 reservoir_sampling.py <k> <input_file> [--verbose]
```

**Arguments:**
- `k`: Sample size (positive integer)
- `input_file`: Path to input file (one element per line)
- `--verbose` (optional): Display detailed processing information

### Examples

**Quiet mode** (displays final sample only):
```bash
python3 reservoir_sampling.py 5 example.txt
```

**Verbose mode** (shows algorithm progression):
```bash
python3 reservoir_sampling.py 5 example.txt --verbose
```

### Sample Output

```
========================================
FINAL SAMPLE
========================================
1. Element 1
2. Element 4
3. Element 7
4. Element 2
5. Element 9
========================================
```

---

## Real-World Applications

- **Log Analysis**: Sample from terabytes of server logs for anomaly detection
- **A/B Testing**: Select random users from continuous user streams
- **Data Mining**: Process web crawl data or sensor feeds without storage limits
- **Recommendation Systems**: Maintain representative user behavior samples
- **Network Monitoring**: Analyze packet streams in real-time

---

## Project Structure

```
Reservoir_Sampling/
├── reservoir_sampling.py    # Main implementation with type hints
├── example.txt              # Example input file (15 sample elements)
└── README.md                # This file
```

---

## Code Quality

This implementation demonstrates professional Python practices:

✅ **Type Hints** - Full type annotations for clarity and IDE support  
✅ **Docstrings** - Comprehensive documentation for all functions  
✅ **Error Handling** - Validates input and handles edge cases  
✅ **Code Organization** - Modular design with single responsibility  
✅ **Variable Naming** - Clear, descriptive names following conventions  
✅ **PEP 8 Compliant** - Professional formatting standards  

---

## Mathematical Proof (Sketch)

**Theorem:** After processing N elements, each element has exactly probability K/N of being in the reservoir.

**Proof by Induction:**

**Base Case (N = K):**
$$P(\text{element in reservoir}) = \frac{K}{K} = 1 \quad \checkmark$$

All K elements are in the reservoir.

**Inductive Hypothesis:**
Assume after processing N elements: $P_N = \frac{K}{N}$

**Inductive Step (N → N+1):**

For any element i that was in the reservoir at step N:

$$P_{\text{stays}} = P_{\text{in at N}} \times P(\text{not replaced at N+1})$$

$$= \frac{K}{N} \times \left(1 - \frac{K}{N} \times \frac{1}{K}\right)$$

$$= \frac{K}{N} \times \left(1 - \frac{1}{N}\right)$$

$$= \frac{K}{N} \times \frac{N-1}{N} = \frac{K(N-1)}{N^2}$$

For the new element at position N+1:

$$P_{\text{new enters}} = \frac{K}{N+1}$$

By the law of total probability, all elements have equal probability:

$$P_{N+1} = \frac{K}{N+1} \quad \checkmark$$

---

## Learning Resources

- **Original Paper:** Vitter, J. S. (1985). "Random Sampling with a Reservoir"
- **Wikipedia:** [Reservoir Sampling](https://en.wikipedia.org/wiki/Reservoir_sampling)
- **Key Concepts:** Streaming algorithms, randomized algorithms, probability theory

---

## License

This project is licensed under the MIT License.