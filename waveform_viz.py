import bilby  # Import bilby for gravitational wave data analysis
import json  # Import json to handle JSON file operations
import matplotlib.pyplot as plt  # Import matplotlib for plotting
import numpy as np  # Import numpy for numerical operations
from main import load_config  # Import the configuration loader function

# Load configuration settings
config = load_config()

def generate_waveform(model, ref_frequency, parameters):
    """
    Generate time-domain waveform using the specified model and parameters.

    Args:
        model (str): The waveform model to use (e.g., "IMRPhenomPv2").
        ref_frequency (float): Reference frequency for waveform generation.
        parameters (dict): Dictionary of parameters for generating the waveform.

    Returns:
        tuple: A tuple containing the plus-polarization time-domain waveform and the time array.
    """
    # Define waveform arguments using the provided model and reference frequency
    waveform_arguments = dict(
        waveform_approximant=model,
        reference_frequency=ref_frequency,
        minimum_frequency=config['minimum_frequency'],
        maximum_frequency=config["maximum_frequency"],
    )
    print(waveform_arguments)  # Print arguments for debugging

    # Create a waveform generator using bilby
    waveform_generator = bilby.gw.WaveformGenerator(
        duration=config["duration"],
        sampling_frequency=config["sampling_frequency"],
        frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
        parameter_conversion=bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters,
        waveform_arguments=waveform_arguments
    )

    # Generate the time-domain strain waveform
    waveform = waveform_generator.time_domain_strain(parameters)
    
    # Return the plus polarization waveform and the corresponding time array
    return waveform['plus'], waveform_generator.time_array

def plot_waveforms(time, waveforms, labels, filename):
    """
    Plot multiple waveforms on the same plot.

    Args:
        time (numpy.ndarray): Array of time values for the x-axis.
        waveforms (list): List of waveforms (numpy arrays) to plot.
        labels (list): List of labels for each waveform to include in the legend.
        filename (str): Filename for saving the plot.

    Returns:
        None. Displays the plot.
    """
    plt.figure(figsize=(10, 6))  # Create a new figure for plotting
    # Plot each waveform with its corresponding label
    for waveform, label in zip(waveforms, labels):
        plt.plot(time, waveform, label=label)
    plt.xlabel('Time [s]')  # Label for the x-axis
    plt.ylabel('Strain')  # Label for the y-axis
    plt.title('Overlay of Time-Domain Waveforms')  # Title of the plot
    plt.legend()  # Add a legend to the plot
    plt.grid(True)  # Show grid lines on the plot
    # Uncomment the next line to save the plot as a file
    # plt.savefig(filename)
    plt.show()  # Display the plot

def main(result_path, injection_model, evaluation_model, ref_frequency):
    """
    Main function to generate and compare waveforms for injected and estimated parameters.

    Args:
        result_path (str): Path to the directory containing the population and results files.
        injection_model (str): Waveform model used for the injected signal.
        evaluation_model (str): Waveform model used for evaluating the signal.
        ref_frequency (float): Reference frequency for waveform generation.

    Returns:
        None. Generates and plots the waveforms.
    """
    # Load the population parameters from a JSON file
    with open(f'{result_path}/population.json', 'r') as f:
        population = json.load(f)
    
    # Load Bilby results from a JSON file
    result = bilby.core.result.read_in_result(filename=f"{result_path}/label_result.json")

    # Iterate over each set of injection parameters in the population
    for i, injection_params in enumerate(population):
        # Generate waveform using the injection model and parameters
        injection_waveform = generate_waveform(injection_model, ref_frequency, injection_params)

        # Generate waveform using the evaluation model and injection parameters
        evaluation_waveform_injection_params = generate_waveform(evaluation_model, ref_frequency, injection_params)

        # Extract estimated parameters from the Bilby result
        estimated_params = result.posterior.iloc[i].to_dict()  # Ensure correct indexing and mapping

        # Generate waveform using the evaluation model and estimated parameters
        evaluation_waveform_estimated_params = generate_waveform(evaluation_model, ref_frequency, estimated_params)

        # Calculate residuals between injection and evaluation waveforms
        resid_both_injection = injection_waveform[0] - evaluation_waveform_injection_params[0]
        resid_injection_evaluation = injection_waveform[0] - evaluation_waveform_estimated_params[0]

        # Plot the waveforms and residuals
        plot_filename = f'waveform_overlay_{i}.png'
        plot_waveforms(
            injection_waveform[1],  # Time array for x-axis
            [resid_both_injection, resid_injection_evaluation],  # List of residual waveforms
            ['Residual eval(injection)', 'Residual eval(estimated)'],  # Labels for the waveforms
            plot_filename  # Filename to save the plot
        )

if __name__ == '__main__':
    # Define the result path and models to use based on the configuration
    result_path = "results"
    injection_model = config["waveform_approximant_injection"]
    evaluation_model = config["waveform_approximant_injection"]  # May need to adjust to a different model if necessary
    ref_frequency = config["reference_frequency"]

    # Run the main function
    main(result_path=result_path, injection_model=injection_model, evaluation_model=evaluation_model, ref_frequency=ref_frequency)
