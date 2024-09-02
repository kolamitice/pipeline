import bilby  # Import bilby for gravitational wave data analysis
import json  # Import json for handling JSON file operations
from bilby.core.prior import Uniform  # Import Uniform prior distribution from bilby

def create_priors(injection_parameters, config):
    """
    Create a dictionary of priors for parameter estimation based on injection parameters and configuration settings.

    Args:
        injection_parameters (dict): Dictionary containing the parameters of the injected gravitational wave signals.
        config (dict): Configuration dictionary specifying which parameters to estimate and their prior bounds.

    Returns:
        bilby.gw.prior.BBHPriorDict: A dictionary of priors for the Bayesian parameter estimation.
    
    The function sets up uniform priors for parameters marked for estimation in the configuration. 
    For parameters not being estimated, it uses their injected values as fixed priors.
    """
    # Initialize a dictionary of priors specific to binary black hole parameters
    priors = bilby.gw.prior.BBHPriorDict()

    # Get the estimation parameters from the configuration
    parameters = config.get("parameters", {})

    # Iterate through each parameter and set the prior based on whether it should be estimated
    for param_name, estimation_bool in parameters.items(): 
        if not estimation_bool["estimate"]:
            # If estimation is False, use the injection parameter value as a fixed prior
            priors[param_name] = injection_parameters[param_name]
        else:
            # If estimation is True, set a Uniform prior within the specified bounds
            priors[param_name] = Uniform(
                injection_parameters[param_name] * config["priors_lower_bound"],  # Lower bound for the uniform prior
                injection_parameters[param_name] * config["priors_upper_bound"],  # Upper bound for the uniform prior
                name=param_name
            )

    # Remove mass ratio and chirp mass from the priors, assuming these are derived parameters
    del priors["mass_ratio"]
    del priors["chirp_mass"]

    print(priors)  # Print the created priors for debugging purposes
    return priors

def run_parameter_estimation(config, result_directory, corner_plot=False):
    """
    Run parameter estimation for a population of gravitational wave signals using Bayesian inference.

    Args:
        config (dict): Configuration dictionary containing settings for parameter estimation, such as waveform arguments,
                       detector setup, and frequency settings.
        result_directory (str): Directory where the results of the parameter estimation will be saved.
        corner_plot(bool): flag to create corner plot defaults to False

    Returns:
        None. Saves the results of the parameter estimation to the specified directory and generates corner plots.
    
    This function reads the population of injection parameters, adjusts the reference frequency if necessary, and 
    performs Bayesian parameter estimation using bilby's built-in sampler and likelihood functions.
    """
    # Load the population parameters from the specified JSON file
    with open(f"{result_directory}/{config['population_file']}", 'r') as f:
        population_parameters = json.load(f)

    # Initialize the reference frequency to start the estimation
    initial_frequency = config["reference_frequency"]

    # Iterate over each set of population parameters
    for i, params in enumerate(population_parameters):
        # Set the geocentric time for each event
        params["geocent_time"] = config["geocent_time"]

        # Create priors for the parameters of the current event
        priors = create_priors(params, config)
        priors["geocent_time"] = config["geocent_time"]

        success = False  # Flag to track successful estimation
        frequency = initial_frequency  # Start with the initial reference frequency

        # Try different reference frequencies until the parameter estimation is successful or the max frequency is reached
        while not success and frequency <= config["max_reference_frequency"]:
            try:
                # Define waveform arguments for signal injection and parameter estimation
                waveform_arguments_injection = dict(
                    waveform_approximant=config['waveform_approximant_injection'],
                    reference_frequency=frequency,
                    minimum_frequency=config['minimum_frequency'],
                    maximum_frequency=config["maximum_frequency"],
                )

                waveform_arguments_estimation = dict(
                    waveform_approximant=config['waveform_approximant_estimation'],
                    reference_frequency=frequency,
                    minimum_frequency=config['minimum_frequency'],
                    maximum_frequency=config["maximum_frequency"],
                )

                # Create waveform generators for injection and estimation
                waveform_injection = bilby.gw.WaveformGenerator(
                    duration=config["duration"],
                    sampling_frequency=config["sampling_frequency"],
                    frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
                    parameter_conversion=bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters,
                    waveform_arguments=waveform_arguments_injection,
                )

                waveform_estimation = bilby.gw.WaveformGenerator(
                    duration=config["duration"],
                    sampling_frequency=config["sampling_frequency"],
                    frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
                    parameter_conversion=bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters,
                    waveform_arguments=waveform_arguments_estimation,
                )

                # Setup interferometers and inject the signal
                ifos = bilby.gw.detector.InterferometerList(config["detector_setup"])
                ifos.set_strain_data_from_power_spectral_densities(
                    sampling_frequency=config["sampling_frequency"],
                    duration=config["duration"],
                    start_time=config["geocent_time"] - 2,
                )
                ifos.inject_signal(
                    waveform_generator=waveform_injection, parameters=params
                )

                # Define the likelihood function for parameter estimation
                likelihood = bilby.gw.GravitationalWaveTransient(
                    interferometers=ifos, waveform_generator=waveform_estimation
                )

                # Run the sampler to perform Bayesian parameter estimation
                result = bilby.run_sampler(
                    likelihood=likelihood,
                    priors=priors,
                    sampler="dynesty",
                    npoints=config["npoints"],
                    injection_parameters=params,
                    outdir=result_directory,
                    resume=False
                )

                # Generate a corner plot to visualize the results of the parameter estimation
                if corner_plot:
                    result.plot_corner(filename=f"{result_directory}/corner_plot_event_{i}.png")
                success = True  # If no error occurs, set success to True

            except Exception as e:
                # If an error occurs, print the error and try the next reference frequency
                print(f"Error with reference frequency {frequency}: {e}")
                frequency += config["frequency_increment"]  # Increment the frequency and try again

        # If no successful estimation is achieved after all attempts
        if not success:
            print(f"Failed to run parameter estimation for event {i} even after adjusting the reference frequency.")