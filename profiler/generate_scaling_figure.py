"""
Generate figures for
"""
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import glob


def load_results():
    norm_values = {
        "wraps": [],
        "steps": [],
        "swaps": [],
        "gifs": [],
        "throughput": [],
    }

    # Load results in variables.
    for t in threads:
        fs = glob.glob(f"results/{results_folder}/{t}_*")
        with open(fs[0], "r") as fp:
            lines = fp.readlines()

            norm_values["wraps"].append(float(lines[1][11:16]))
            norm_values["steps"].append(float(lines[2][11:16]))
            norm_values["swaps"].append(float(lines[3][11:16]))
            norm_values["gifs"].append(float(lines[4][11:16]))
            norm_values["throughput"].append(float(lines[8][12:18]))

    return norm_values


def gen_scaling_plot():
    # Arrays with measured values.
    data = load_results()

    # # Normalize the arrays.
    # metrics = ["wraps", "steps", "swaps", "gifs"]
    # for _ in versions:
    #     total = sum([norm_values[m][0] for m in metrics])
    #     for m in metrics:
    #         norm_values[m].append(norm_values[m][0]/total)
    #         norm_values[m].pop(0)

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
