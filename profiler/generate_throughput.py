"""
Generate figures for throughput plots.
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
    for v in versions:
        fs = glob.glob(f"results/{results_folder}/{v}_*")
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


def gen_throughput():
    # Arrays with measured values.
    norm_values = load_results()

    # Create DataFrame with normalized performance numbers.
    df = pd.DataFrame({"Version": versions,
                       "throughput": norm_values["throughput"]})

    sns.set(style="white")
    ax = sns.barplot(x="Version", y="throughput", data=df, color="#4878D0")

    # Compose values per 1000.
    bar_values = []
    for rec in ax.containers[0]:
        txt = str(round(rec.get_height(), -3))[:-5] + "K"
        ax.text(x=rec.get_x() + rec.get_width() / 2, y=rec.get_height()+.5,
                s=txt, ha="center")

    # Add info to plot.
    plt.title("Throughput per version", fontsize=16)
    plt.xlabel("Versions", labelpad=0)
    plt.ylabel("Throughput (pixels/second)")
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt_ax = plt.gca()
    plt_ax.tick_params(axis="both", which="major", pad=0)

    # Compose ylabel per 1000.
    ylbls = ax.get_yticklabels()
    new_labels = []
    for ylbl in ylbls:
        new_labels.append(str(round(float(ylbl.get_text()), -3))[:-5] + "K")
    ax.set_yticklabels(new_labels)

    # Save and show plot.
    plt.savefig(f"figures/{results_folder}_throughput_{'-'.join(versions)}")
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

    # Generate throughput plot with the given versions.
    gen_throughput()
