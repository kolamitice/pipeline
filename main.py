import os
from generate_population import generate_population
from parameter_estimation import run_parameter_estimation
from bias_calculation import calculate_bias
import yaml 

def load_config(config_file='config.yaml'):
    # Load the YAML configuration
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    return config

def create_results_directory(base_dir):
    if not os.path.exists(base_dir):
        print("Creating new directory {base_dir} to store results...")
        os.makedirs(base_dir)
        return base_dir

    i = 1
    new_dir = f"{base_dir}_{i}"

    while os.path.exists(new_dir):
        i += 1
        new_dir = f"{base_dir}_{i}"

    print(f"{base_dir} already exists. Creating new directory {base_dir} to store results...")
    os.makedirs(new_dir)
    return new_dir

def main():
    # Load the configuration
    config = load_config()

    # Ensure results directory exists
    dir = create_results_directory(config['results_dir'])

    # Step 1: Generate the population
    print("Generating the population of IMBH binaries...")
    generate_population(config=config, result_directory=dir)
    
    # Step 2: Perform parameter estimation for each event
    print("Running parameter estimation for each event in the population...")
    run_parameter_estimation(config=config, result_directory=dir)
    
    # Step 3: Calculate biases based on the estimation results
    print("Calculating biases for the estimated parameters...")
    calculate_bias(config=config, result_directory=dir)

    print("All steps completed successfully. The bias results are saved in", config['bias_output_file'])

if __name__ == "__main__":
    main()
