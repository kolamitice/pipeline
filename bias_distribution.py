import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file into a DataFrame
data = pd.read_csv('results_7/biases.csv')

# Extract non-zero bias values for 'mass_1'
mass_1_bias = data['mass_1']

# Plot the bias distribution for 'mass_1'
plt.figure(figsize=(10, 6))
plt.hist(mass_1_bias, bins=2, color='blue', alpha=0.7, edgecolor='black')
plt.title('Bias Distribution for mass_1')
plt.xlabel('Bias (mass_1)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
