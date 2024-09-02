import numpy as np  # Import numpy for numerical operations
import json  # Import json to handle JSON file operations

def generate_population(config, result_directory):
    """
    Generate a population of intermediate-mass black hole (IMBH) binaries based on given configuration.

    Args:
        config (dict): Configuration dictionary containing parameters for population generation. 
                       It should have the following keys:
                       - "num_events" (int): Number of events to generate.
                       - "parameters" (dict): Dictionary where each key is a parameter name and the value is a dictionary 
                         with "min" and "max" values defining the range of that parameter.
                       - "population_file" (str): Name of the file to save the generated population data.
        result_directory (str): Directory where the resulting population file will be saved.

    Returns:
        None. The generated population data is saved to a JSON file specified by the 'population_file' key in the config.
    
    The function generates random parameters for each event within the specified bounds 
    and saves the generated population to a JSON file.
    """
    
    # Extract the number of events to generate from the configuration
    num_events = config["num_events"]

    # Initialize a list to store parameters for each event
    population_parameters = []

    # Generate random parameters for each event
    for _ in range(num_events):
        params = {}  # Dictionary to store parameters for a single event
        parameters = config.get("parameters", {})  # Get parameter ranges from the configuration

        # Generate random values for each parameter within the specified bounds
        for param_name, bounds in parameters.items():
            params[param_name] = np.random.uniform(bounds.get("min"), bounds.get("max"))
        
        # Append the generated parameters for the event to the population list
        population_parameters.append(params)

    # Save the generated population to a JSON file
    with open(f"{result_directory}/{config['population_file']}", 'w') as f:
        json.dump(population_parameters, f, indent=4)

    # Print a message indicating the successful generation and saving of the population data
    print(f"Population of {num_events} IMBH binaries generated and saved to {result_directory}/{config['population_file']}")

# The following block allows the script to be run independently but is incomplete here.
if __name__ == "__main__":
    # Example configuration and result directory should be defined here to run the function
    generate_population()