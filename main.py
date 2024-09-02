import os  # Import os for handling file and directory operations
from generate_population import generate_population  # Import function to generate population
from parameter_estimation import run_parameter_estimation  # Import function to run parameter estimation
from bias_calculation import calculate_bias  # Import function to calculate bias
import yaml  # Import yaml for loading configuration files

def load_config(config_file='config.yaml'):
    """
    Load the YAML configuration file.

    Args:
        config_file (str): Path to the YAML configuration file. Defaults to 'config.yaml'.

    Returns:
        dict: A dictionary containing the configuration settings loaded from the YAML file.
    """
    # Load the YAML configuration
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    return config

def create_results_directory(base_dir):
    """
    Create a new results directory to store output files. If the base directory already exists, 
    creates a new directory with an incremented suffix.

    Args:
        base_dir (str): The base directory path where results should be stored.

    Returns:
        str: The path of the created results directory.
    """
    # Check if the base directory exists
    if not os.path.exists(base_dir):
        print(f"Creating new directory {base_dir} to store results...")
        os.makedirs(base_dir)  # Create the base directory if it does not exist
        return base_dir

    # If the directory exists, create a new one with an incremented suffix
    i = 1
    new_dir = f"{base_dir}_{i}"

    # Increment the suffix until a non-existing directory name is found
    while os.path.exists(new_dir):
        i += 1
        new_dir = f"{base_dir}_{i}"

    print(f"{base_dir} already exists. Creating new directory {new_dir} to store results...")
    os.makedirs(new_dir)  # Create the new directory
    return new_dir

def main():
    """
    Main function to run the full pipeline for gravitational wave analysis.
    This includes generating a population of events, running parameter estimation for each event,
    and calculating biases for the estimated parameters.
    """
    # Load the configuration from the YAML file
    config = load_config()

    # Ensure the results directory exists or create a new one
    dir = create_results_directory(config['results_dir'])

    # Step 1: Generate the population of intermediate-mass black hole (IMBH) binaries
    print("Generating the population of IMBH binaries...")
    generate_population(config=config, result_directory=dir)
    
    # Step 2: Perform parameter estimation for each event in the population
    print("Running parameter estimation for each event in the population...")
    run_parameter_estimation(config=config, result_directory=dir)
    
    # Step 3: Calculate biases based on the estimation results
    print("Calculating biases for the estimated parameters...")
    calculate_bias(config=config, result_directory=dir)

    # Indicate completion of all steps
    print("All steps completed successfully. The bias results are saved in", config['bias_output_file'])

if __name__ == "__main__":
    # Run the main function when the script is executed
    main()
