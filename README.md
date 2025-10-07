# Stochastic Process Visualization Engine

The Stochastic Process Visualization Engine is a Python application designed for exploring and understanding randomness and statistical bias. It generates datasets with specific, subtle biases and provides a suite of tools to visualize and analyze the data, challenging the user to identify the underlying pattern.

The application features two modes: a rich graphical user interface (GUI) for interactive exploration and a command-line interface (CLI) for headless analysis and scripting.

<img width="943" height="610" alt="image" src="https://github.com/user-attachments/assets/2e9f9f84-552a-46cb-be8c-d46daa4a02a8" />

```bash
Stochastic-Process-Visualization-Engine (main) $ python main.py --cli
Running in Command-Line Interface (CLI) mode.

Generating 1000 data points...
Generated data with bias: 'Uniform - True uniform distribution' (ID: 8)

Running statistical analysis...

-------------------- Statistical Analysis Results --------------------
  - Skewness                  | Value: -0.0525         | Status: PASSED
  - Kurtosis                  | Value: -1.1440         | Status: FAILED
  - Shannon Entropy           | Value: 6.5843          | Status: PASSED
  - Chi-Square Uniformity     | Value: 18.2800         | Status: PASSED
  - KS Test (Uniform)         | Value: 0.0335          | Status: PASSED
  - Z-Score Deviation         | Value: 0.8572          | Status: PASSED
----------------------------------------------------------------------
Stochastic-Process-Visualization-Engine (main) $ python main.py --cli --bias-id 3
Running in Command-Line Interface (CLI) mode.

Generating 1000 data points...
Generated data with bias: 'Bell Curve - Normal distribution centered at 5000' (ID: 3)

Running statistical analysis...

-------------------- Statistical Analysis Results --------------------
  - Skewness                  | Value: 0.0795          | Status: PASSED
  - Kurtosis                  | Value: 0.0740          | Status: PASSED
  - Shannon Entropy           | Value: 5.8502          | Status: FAILED
  - Chi-Square Uniformity     | Value: 957.9600        | Status: FAILED
  - KS Test (Uniform)         | Value: 0.2211          | Status: FAILED
  - Z-Score Deviation         | Value: 1.1688          | Status: PASSED
----------------------------------------------------------------------
Stochastic-Process-Visualization-Engine (main) $ python main.py --cli --count 5000
Running in Command-Line Interface (CLI) mode.

Generating 5000 data points...
Generated data with bias: 'Uniform - True uniform distribution' (ID: 8)

Running statistical analysis...

-------------------- Statistical Analysis Results --------------------
  - Skewness                  | Value: -0.0299         | Status: PASSED
  - Kurtosis                  | Value: -1.1970         | Status: FAILED
  - Shannon Entropy           | Value: 6.6281          | Status: PASSED
  - Chi-Square Uniformity     | Value: 18.0080         | Status: PASSED
  - KS Test (Uniform)         | Value: 0.0137          | Status: PASSED
  - Z-Score Deviation         | Value: 1.0573          | Status: PASSED
----------------------------------------------------------------------
Stochastic-Process-Visualization-Engine (main) $ python main.py --list-biases
Running in Command-Line Interface (CLI) mode.

Available bias patterns:
  ID 1: Clustered Low - 70% between 0-3000
  ID 2: Clustered High - 70% between 7000-10000
  ID 3: Bell Curve - Normal distribution centered at 5000
  ID 4: Periodic Spikes - Every 100th value is 9999
  ID 5: Missing Ranges - Omit numbers between 3000-4000
  ID 6: Even-Heavy - 80% even numbers
  ID 7: Prime-Rich - 50% prime numbers
  ID 8: Uniform - True uniform distribution
```

## Features

- **Biased Data Generation**: Creates datasets with one of several underlying bias patterns:
  - Clustered distributions (low or high)
  - Bell curve (normal distribution)
  - Periodic spikes
  - Missing numerical ranges
  - Even/odd number prevalence
  - Prime number prevalence
  - True uniform distribution
- **Interactive Visualization**: A histogram dynamically displays the distribution of the generated data, providing immediate visual clues.
- **Comprehensive Statistical Analysis**: Runs a battery of statistical tests on the data, including:
  - Skewness and Kurtosis
  - Shannon Entropy
  - Chi-Square and Kolmogorov-Smirnov uniformity tests
  - Z-Score Deviation
  - Autocorrelation
- **Inference Challenge**: A game-like feature where the user guesses the bias based on the visual and statistical evidence, receiving a score for their accuracy.
- **Dual-Mode Operation**:
  - **GUI Mode**: A full-featured graphical interface built with Tkinter for interactive use.
  - **CLI Mode**: A headless mode for generating data and running analysis directly from the terminal, perfect for scripting and automated testing.
- **Export Results**: Save inference results, including statistical test outputs, to a JSON file.

## Requirements

- Python 3.8+
- Dependencies are listed in `requirements.txt`.

Install the required libraries using pip:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Mode

To run the application in its graphical mode, simply execute the `main.py` script without any arguments. This requires a desktop environment.

```bash
python main.py
```

### Command-Line Interface (CLI) Mode

The CLI mode is ideal for headless environments or for scripting.

**List available bias patterns and their IDs:**
```bash
python main.py --list-biases
```

**Run analysis with a random bias and 5000 data points:**
```bash
python main.py --cli --count 5000
```

**Run analysis for a specific bias (e.g., ID 4: Periodic Spikes):**
```bash
python main.py --cli --bias-id 4
```
