import bilby
import json
import matplotlib.pyplot as plt
import numpy as np
from main import load_config

config = load_config()

def generate_waveform(model, ref_frequency, parameters):
    """Generate time-domain waveform using the given model and parameters."""
    waveform_arguments = dict(
        waveform_approximant=model,
        reference_frequency = ref_frequency,
        minimum_frequency=config['minimum_frequency'],
        maximum_frequency=config["maximum_frequency"],
    )
    print(waveform_arguments)
    waveform_generator = bilby.gw.WaveformGenerator(
        duration=config["duration"],
        sampling_frequency=config["sampling_frequency"],
        frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
        parameter_conversion=bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters,
        waveform_arguments=waveform_arguments
    )
    waveform = waveform_generator.time_domain_strain(parameters)
    return waveform['plus'], waveform_generator.time_array

def plot_waveforms(time, waveforms, labels, filename):
    """Plot multiple waveforms on the same plot."""
    plt.figure(figsize=(10, 6))
    for waveform, label in zip(waveforms, labels):
        plt.plot(time, waveform, label=label)
    plt.xlabel('Time [s]')
    plt.ylabel('Strain')
    plt.title('Overlay of Time-Domain Waveforms')
    plt.legend()
    plt.grid(True)
    #plt.savefig(filename)
    plt.show()

def main(result_path, injection_model, evaluation_model, ref_frequency):
    # Load the population file
    with open(f'{result_path}/population.json', 'r') as f:
        population = json.load(f)
    
    # Load Bilby results
    result = bilby.core.result.read_in_result(filename=f"{result_path}/label_result.json")

    for i, injection_params in enumerate(population):
        # Generate waveform with injection model using injection parameters
        injection_waveform = generate_waveform(injection_model, ref_frequency, injection_params)

        # Generate waveform with evaluation model using injection parameters
        evaluation_waveform_injection_params = generate_waveform(evaluation_model, ref_frequency, injection_params)
        #Extract estimated parameters from Bilby result
        estimated_params = result.posterior.iloc[i].to_dict()  # Ensure correct indexing and mapping
        evaluation_waveform_estimated_params = generate_waveform(evaluation_model, ref_frequency, estimated_params)
        resid_both_injection = injection_waveform[0] - evaluation_waveform_injection_params[0]
        resid_injection_evaluation = injection_waveform[0] - evaluation_waveform_estimated_params[0]
        # Plot the waveforms
        plot_filename = f'waveform_overlay_{i}.png'
        plot_waveforms(
            injection_waveform[1],
            [resid_both_injection, resid_injection_evaluation],
            ['Residual eval(injection)', 'Residual eval(estimated)'],
            plot_filename
        )

if __name__ == '__main__':
    result_path = "results_7"
    injection_model = config["waveform_approximant_injection"]
    evaluation_model = config["waveform_approximant_injection"]
    ref_frequency = config["reference_frequency"]
    main(result_path=result_path, injection_model=injection_model, evaluation_model=evaluation_model, ref_frequency=ref_frequency)
