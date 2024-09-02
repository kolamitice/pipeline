import json  # Import json to handle JSON file operations
import pandas as pd  # Import pandas for data manipulation and analysis
import os  # Import os to handle file operations
import bilby  # Import bilby for gravitational wave data analysis

def calculate_bias(config, result_directory):
    """
    Calculate the bias between the true and estimated values of gravitational wave parameters.

    Args:
        config (dict): Configuration dictionary containing information about the population file and output bias file.
                       It should have the following keys:
                       - "population_file" (str): Name of the file containing the true population parameters.
                       - "bias_output_file" (str): Name of the file to save the calculated biases.
        result_directory (str): Directory where the results and population files are stored.

    Returns:
        None. The calculated biases are saved to a CSV file specified by the 'bias_output_file' key in the config.

    This function reads the true parameters from a population file, compares them with the estimated values from
    result files, and calculates the bias for each parameter. The biases are saved to a CSV file.
    """
    # Load the true population parameters from the specified JSON file
    with open(f"{result_directory}/{config['population_file']}", 'r') as f:
        population_parameters = json.load(f)

    biases = []  # List to store bias for each event

    # Iterate over each set of population parameters
    for i, params in enumerate(population_parameters):
        # Define the path to the result file for the current event
        result_file = f"{result_directory}/label_result.json"  # Assumes a common result file; modify if necessary
        
        # Check if the result file exists
        if os.path.exists(result_file):
            # Read in the result file using bilby's function
            result = bilby.result.read_in_result(result_file)
            posterior = result.posterior  # Access the posterior distribution

            biases_event = {}  # Dictionary to store biases for the current event
            
            # Calculate bias for each parameter
            for param in params.keys():
                estimated_value = posterior[param].mean()  # Calculate the mean of the posterior for the parameter
                true_value = params[param]  # Get the true value from the population parameters
                bias = estimated_value - true_value  # Calculate the bias
                biases_event[param] = bias  # Store the bias in the dictionary

            biases.append(biases_event)  # Append the biases for the event to the list

    # Convert the list of biases to a DataFrame
    bias_df = pd.DataFrame(biases)
    print(bias_df)  # Print the DataFrame for inspection

    # Save the DataFrame to a CSV file
    bias_df.to_csv(f"{result_directory}/{config['bias_output_file']}", index=True)
    print(f"Bias calculation completed and saved to {result_directory}/{config['bias_output_file']}")

if __name__ == "__main__":
    # Example configuration and result directory for running the function
    config = {}
    result_directory = "results_5"
    config["bias_output_file"] = "biases.csv"
    config["population_file"] = "population.json"

    # Run the bias calculation function with the example configuration
    calculate_bias(config, result_directory=result_directory)