import pandas as pd  # Import pandas for data manipulation and analysis
import matplotlib.pyplot as plt  # Import matplotlib for plotting

def plot_bias_distributions(csv_file_path, columns, bins):
    """
    Load bias data from a CSV file and plot the bias distributions for specified parameters in two separate subplots within the same figure.

    Args:
        csv_file_path (str): Path to the CSV file containing bias data.
        columns (list): List of two column names to plot.

    Returns:
        None. Displays a figure with two subplots of the bias distributions for the specified parameters.
    """
    # Load the data from the CSV file into a DataFrame
    data = pd.read_csv(csv_file_path)

    # Ensure that exactly two columns are specified
    if len(columns) != 2:
        raise ValueError("Please provide exactly two column names for plotting.")

    # Set up the subplots in a single figure with 1 row and 2 columns
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Loop through each bias column and plot the bias distribution in separate subplots
    for i, column in enumerate(columns):
        # Extract bias values for the current parameter
        bias_values = data[column]

        # Plot the bias distribution for the current parameter in a subplot
        axes[i].hist(bias_values, bins=bins, color='blue', alpha=0.7, edgecolor='black')  # Plot the histogram
        axes[i].set_title(f'Bias Distribution for {column}')  # Set the title dynamically based on the column
        axes[i].set_xlabel(f'Bias ({column})')  # Set the x-axis label dynamically based on the column
        axes[i].set_ylabel('Frequency')  # Set the y-axis label
        axes[i].grid(True)  # Enable grid for better visualization

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.show()  # Display the figure with subplots

if __name__ == "__main__":
    # Specify the path to the CSV file containing bias data
    csv_file_path = 'results_3/biases.csv'
    # Specify the list of two columns to plot
    columns = ["mass_1", "mass_2"]  # Example columns; modify as needed
    # number of bins in the histogramm
    bins = 20
    # Call the function to plot bias distributions
    plot_bias_distributions(csv_file_path, columns, bins)
