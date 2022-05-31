"""
Generate figures for scaling plots.
"""
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import glob


def load_results():
    values = {
        "inits": [],
        "wraps": [],
        "steps": [],
        "swaps": [],
        "gifs": [],
        "finals": [],
        "throughput": [],
    }

    # Load results in variables.
    for t in threads:
        fs = glob.glob(f"results/{results_folder}/{t}_*")
        with open(fs[0], "r") as fp:
            lines = fp.readlines()

            values["inits"].append(float(lines[1][11:16]))
            values["wraps"].append(float(lines[2][11:16]))
            values["steps"].append(float(lines[3][11:16]))
            values["swaps"].append(float(lines[4][11:16]))
            values["gifs"].append(float(lines[5][11:16]))
            values["finals"].append(float(lines[6][11:16]))
            values["throughput"].append(float(lines[10][12:18]))

    return values


def gen_scaling_plot():
    # Arrays with measured values.
    data = load_results()

    # Create DataFrame with normalized performance numbers.
    df = pd.DataFrame({"nthreads": threads,
                       "wrap": data["wraps"],
                       "step": data["steps"],
                       "swap": data["swaps"],
                       "gif":  data["gifs"]})

    # Setup stacked barchart.
    sns.set(style="white")
    df.set_index("nthreads").plot(kind="bar", stacked=True)

    # Add info to plot.
    plt.title("Time spend per number of threads", fontsize=16)
    plt.xlabel("Number of threads", labelpad=0)
    plt.ylabel("Time spend (s)")
    plt.xticks(rotation=0)
    ax = plt.gca()
    ax.tick_params(axis="both", which="major", pad=0)
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    # Save and show plot.
    plt.savefig(f"figures/{results_folder}_{'-'.join(threads)}")
    plt.show()


if __name__ == "__main__":
    # Get results folder and versions from command line.
    args = sys.argv
    results_folder = args[1]
    threads = args[2:]

    # Check for existence of results folder.
    if not os.path.isdir(f"results/{results_folder}"):
        print(f"Given results folder '{results_folder}' does not exist..")
        exit(1)

    # Check for existence of all version results.
    for t in threads:
        files = glob.glob(f"results/{results_folder}/{t}_*")
        if len(files) == 0:
            print(f"Results for '{t}' threads do not exist..")
            exit(1)

    # # Generate normalized bar plot with the given versions.
    gen_scaling_plot()