import json
import pandas as pd
import os
import bilby

def calculate_bias(config, result_directory):
    with open(f"{result_directory}/{config['population_file']}", 'r') as f:
        population_parameters = json.load(f)

    biases = []
    for i, params in enumerate(population_parameters):
        result_file = f"{result_directory}/label_result.json"
        if os.path.exists(result_file):
            result = bilby.result.read_in_result(result_file)
            posterior = result.posterior
            biases_event = {}
            for param in params.keys():
                estimated_value = posterior[param].mean()
                true_value = params[param]
                bias = estimated_value - true_value
                biases_event[param] = bias
            biases.append(biases_event)

    bias_df = pd.DataFrame(biases)
    print(bias_df)
    bias_df.to_csv(f"{result_directory}/{config['bias_output_file']}", index=True)
    print(f"Bias calculation completed and saved to {result_directory}/{config['bias_output_file']}")

if __name__=="__main__":
    config = {}
    result_directory = "results_5"
    config["bias_output_file"] = "biases.csv"
    config["population_file"] = "population.json"

    calculate_bias(config, result_directory=result_directory)
