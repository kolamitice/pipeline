import numpy as np
import json

def generate_population(config, result_directory):
    num_events = config["num_events"]
    population_parameters = []
    for _ in range(num_events):
        params = {}
        parameters = config.get("parameters", {})
        for param_name, bounds in parameters.items():
            params[param_name] = np.random.uniform(bounds.get("min"), bounds.get("max"))
        population_parameters.append(params)

    with open(f"{result_directory}/{config['population_file']}", 'w') as f:
        json.dump(population_parameters, f, indent=4)

    print(f"Population of {num_events} IMBH binaries generated and saved to {config['results_dir']}/{config['population_file']}")

if __name__ == "__main__":
    generate_population()