import bilby
import json
from bilby.core.prior import Uniform

def create_priors(injection_parameters, config):
    priors = bilby.gw.prior.BBHPriorDict()
    parameters = config.get("parameters", {})
    for param_name, estimation_bool in parameters.items(): 
        if not estimation_bool["estimate"]:
            priors[param_name] = injection_parameters[param_name]
        else:
            priors[param_name] = Uniform(injection_parameters[param_name] * config["priors_lower_bound"], injection_parameters[param_name] * config["priors_upper_bound"], name=param_name)

    del priors["mass_ratio"]
    del priors["chirp_mass"]
    print(priors)
    return priors

def run_parameter_estimation(config, result_directory):
    with open(f"{result_directory}/{config['population_file']}", 'r') as f:
        population_parameters = json.load(f)

    initial_frequency = config["reference_frequency"]  # Start with the initial reference frequency

    for i, params in enumerate(population_parameters):
        params["geocent_time"] = config["geocent_time"]
        priors = create_priors(params, config)
        priors["geocent_time"] = config["geocent_time"]

        success = False
        frequency = initial_frequency

        while not success and frequency <= config["max_reference_frequency"]:
            try:
                # Adjust waveform arguments with the current reference frequency
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

                ifos = bilby.gw.detector.InterferometerList(config["detector_setup"])
                ifos.set_strain_data_from_power_spectral_densities(
                    sampling_frequency=config["sampling_frequency"],
                    duration=config["duration"],
                    start_time=config["geocent_time"] - 2,
                )
                ifos.inject_signal(
                    waveform_generator=waveform_injection, parameters=params
                )

                likelihood = bilby.gw.GravitationalWaveTransient(
                    interferometers=ifos, waveform_generator=waveform_estimation
                )

                result = bilby.run_sampler(
                    likelihood=likelihood,
                    priors=priors,
                    sampler="dynesty",
                    npoints=config["npoints"],
                    injection_parameters=params,
                    outdir=result_directory,
                    resume=False
                )

                result.plot_corner(filename=f"{result_directory}/corner_plot_event_{i}.png")
                success = True  # If no error occurs, set success to True

            except Exception as e:
                print(f"Error with reference frequency {frequency}: {e}")
                frequency += config["frequency_increment"]  # Increment the frequency and try again

        if not success:
            print(f"Failed to run parameter estimation for event {i} even after adjusting the reference frequency.")