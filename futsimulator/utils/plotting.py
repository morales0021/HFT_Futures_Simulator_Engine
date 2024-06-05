# Step 2: Import the necessary modules
import matplotlib.pyplot as plt
import pdb


def get_plot(values, x_label, y_label, title, pathfile):
    # Step 4: Create the plot
    for sub_title, list_val in values.items():
        plt.plot(list_val, label = sub_title)

    # Step 5: Add labels and title (optional)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.title(title)

    # Step 6: Save the plot as a PNG file
    plt.savefig(pathfile)
    plt.clf()