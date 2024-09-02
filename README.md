# Gravitational Wave Analysis Pipeline

This repository provides a comprehensive pipeline for analyzing gravitational wave signals, specifically focusing on intermediate-mass black hole (IMBH) binaries. The pipeline includes population generation, parameter estimation, bias calculation, and waveform visualization. The workflow is designed using the `bilby` library, a Bayesian inference library for gravitational-wave astronomy.

## Overview

The pipeline performs the following steps:

1. **Population Generation**: Generates a synthetic population of gravitational wave signals (events) based on user-defined parameters.
2. **Parameter Estimation**: Uses Bayesian inference to estimate the parameters of each event from the synthetic population.
3. **Bias Calculation**: Calculates the bias between true and estimated parameters for each event.
4. **Waveform Generation and Visualization**: Generates waveforms for both injected and estimated parameters and visualizes their differences.

## Capabilities

- **Generate Synthetic Populations**: Customize the number of events, parameter ranges, and other settings to generate a synthetic population of gravitational wave signals.
- **Bayesian Parameter Estimation**: Uses the `bilby` library to perform Bayesian inference, providing posterior distributions for each parameter.
- **Bias Calculation**: Computes the bias between true injected parameters and estimated parameters for various physical parameters.
- **Waveform Visualization**: Generate and visualize time-domain waveforms for injected and estimated parameters to study residuals and differences.
- **Flexible Configuration**: All settings, such as parameter ranges, estimation options, waveform models, and more, are controlled through a configuration file (`config.yaml`).

## Installation

To use this pipeline, you need to have the following dependencies installed:

- `Python 3.8` or higher
- `bilby`
- `numpy`
- `scipy`
- `matplotlib`
- `pandas`
- `pyyaml`

Install the dependencies:

```bash
pip install requirements.txt
```

If you want to use the model `NRSur7dq4` run the following commands:

```bash
python download_surrogate.py
export LAL_DATA_PATH=~/lal_data
```
this will download the model as .h5 file and stores it into the correct path for LALSimulation library to access it.

# Configuration File

The configuration for the pipeline is provided in a `config.yaml` file. This file contains all the necessary parameters for waveform generation, population generation, parameter estimation, and bias calculation. Here is an overview of the configuration options:

## Key Configuration Parameters

### Waveform Settings:

- `waveform_approximant_estimation`: Waveform model used for parameter estimation (e.g., `"IMRPhenomPv2"`).
- `waveform_approximant_injection`: Waveform model used for signal injection (e.g., `"IMRPhenomPv2"`).
- `reference_frequency`: Reference frequency for parameter estimation, in Hz.
- `max_reference_frequency`: Maximum reference frequency, in Hz.
- `reference_frequency_steps`: Step size for incrementing reference frequency, in Hz.
- `minimum_frequency`: Minimum frequency for waveform generation, in Hz.
- `maximum_frequency`: Maximum frequency for waveform generation, in Hz.
- `sampling_frequency`: Sampling frequency for data, in Hz.
- `geocent_time`: Geocentric time of the coalescence in GPS seconds.
- `duration`: Duration of the waveform in seconds.

### Population Generation Settings:

- `num_events`: Number of synthetic events to generate.
- `priors_lower_bound` / `priors_upper_bound`: Multipliers for setting uniform priors around injected values.

### Parameter Estimation Settings:

- `detector_setup`: List of detectors used (e.g., `["H1", "L1"]` for LIGO Hanford and Livingston).
- `npoints`: Number of live points for the Bayesian sampler.

### File Paths:

- `population_file`: Path to the file where the population data will be saved.
- `results_dir`: Directory where results will be saved.
- `bias_output_file`: Path to the file where the bias results will be saved.

### Parameter Specification for Population and Estimation:

- `parameters`: Dictionary specifying each parameter, whether to estimate it (`true` or `false`), and its minimum and maximum values for population generation.

# How to Use the Pipeline

## Step 1: Configure the `config.yaml` File

Before running the pipeline, customize the `config.yaml` file according to your requirements. This file controls all the settings for the population generation, parameter estimation, and bias calculation.

## Step 2: Run the Main Pipeline

The pipeline can be run using the `main.py` script, which orchestrates all the steps:

1. **Generate the Population**: This step generates a synthetic population of gravitational wave events based on the parameters specified in the `config.yaml` file.
   
2. **Run Parameter Estimation**: This step performs Bayesian parameter estimation on each generated event using the `bilby` library.
   
3. **Calculate Biases**: This step calculates the bias between true and estimated parameters for each event and saves the results to a CSV file.

To run the pipeline, execute the following command:

```bash
python main.py
```

## Step 3: Visualize the Results

After running the pipeline, the results, including posterior distributions and bias calculations, will be saved in the `results_dir` directory specified in the configuration file. You can visualize the results using the waveform visualization tools provided.

To visualize the waveform residuals between injected and estimated parameters, use the `plot_waveforms.py` script:

To visualize the bias distribution, use the `bias_distribution.py` script:

```bash
python plot_waveforms.py
python bias_distribution.py
```
## Detailed Explanation of Each Step

### 1. Generate Population (`generate_population.py`)

This script generates a synthetic population of IMBH (Intermediate-Mass Black Hole) binaries. It uses the following steps:

- Reads configuration parameters from `config.yaml`.
- For each event, randomly generates parameters (e.g., mass, spin, distance) within specified bounds.
- Saves the generated population to `population_file`.

### 2. Parameter Estimation (`parameter_estimation.py`)

This script performs parameter estimation for each event in the generated population:

- Loads the population from `population_file`.
- Uses `bilby` to perform Bayesian inference for each event.
- Adjusts the reference frequency iteratively to find the optimal setting for parameter estimation.
- Saves the posterior distributions and corner plots to the results directory.

### 3. Bias Calculation (`bias_calculation.py`)

This script calculates the bias between the true injected parameters and the estimated parameters:

- Reads the true parameters from `population_file`.
- Reads the estimated parameters from `label_result.json` files generated by `bilby`.
- Computes the bias for each parameter and saves the results to `bias_output_file`.

### 4. Waveform Generation and Visualization (`waveform_viz.py`)

This script generates and visualizes time-domain waveforms for injected and estimated parameters:

- Loads the population and results.
- Generates waveforms using both the injection and estimation models.
- Plots the residuals to help understand the differences between the injected and estimated signals.


