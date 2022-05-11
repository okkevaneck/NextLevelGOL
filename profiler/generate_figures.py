"""
Generate figures for
"""
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import glob


def load_results(v):
    fs = glob.glob(f"results/{results_folder}/{v}_*")
    with open(fs[0], "r") as fp:
        values = {}
        lines = fp.readlines()
        values["wrap"] = float(lines[1][11:16])
        values["step"] = float(lines[2][11:16])
        values["swap"] = float(lines[3][11:16])
        values["gif"] = float(lines[4][11:16])

    return values


def gen_barplot():
    # Arrays with normalized values.
    norm_values = {
        "wraps": [],
        "steps": [],
        "swaps": [],
        "gifs": [],
    }

    # Load results in variables.
    timings = {}
    for v in versions:
        timings[v] = load_results(v)
        norm_values["wraps"].append(timings[v]["wrap"])
        norm_values["steps"].append(timings[v]["step"])
        norm_values["swaps"].append(timings[v]["swap"])
        norm_values["gifs"].append(timings[v]["gif"])

    # Normalize the arrays.
    metrics = ["wraps", "steps", "swaps", "gifs"]
    for _ in versions:
        total = sum([norm_values[m][0] for m in metrics])
        for m in metrics:
            norm_values[m].append(norm_values[m][0]/total)
            norm_values[m].pop(0)

    # Create DataFrame with normalized performance numbers.
    df = pd.DataFrame({"Version": versions,
                       "wrap": norm_values["wraps"],
                       "step": norm_values["steps"],
                       "swap": norm_values["swaps"],
                       "gif":  norm_values["gifs"]})

    # Setup stacked barchart.
    sns.set(style="white")
    df.set_index("Version").plot(kind="bar", stacked=True)

    # Add info to plot.
    plt.title("Relative time spend per version", fontsize=16)
    plt.xlabel("Versions", labelpad=0)
    plt.ylabel("Relative time spend")
    plt.xticks(rotation=45)
    plt.gca().tick_params(axis="both", which="major", pad=0)

    # Save and show plot.
    plt.savefig(f"figures/{results_folder}_{'-'.join(versions)}")
    plt.show()


if __name__ == "__main__":
    # Get results folder and versions from command line.
    args = sys.argv
    results_folder = args[1]
    versions = args[2:]

    # Check for existence of results folder.
    if not os.path.isdir(f"results/{results_folder}"):
        print(f"Given results folder '{results_folder}' does not exist..")
        exit(1)

    # Check for existence of all version results.
    for ver in versions:
        files = glob.glob(f"results/{results_folder}/{ver}_*")
        if len(files) == 0:
            print(f"Results for version '{ver}' do not exist..")
            exit(1)

    # Generate normalized bar plot with the given versions.
    gen_barplot()
