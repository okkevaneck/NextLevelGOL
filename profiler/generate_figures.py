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
    for v in versions:
        fs = glob.glob(f"results/{results_folder}/{v}_*")
        with open(fs[0], "r") as fp:
            lines = fp.readlines()

            norm_values["wraps"].append(float(lines[1][11:16]))
            norm_values["steps"].append(float(lines[2][11:16]))
            norm_values["swaps"].append(float(lines[3][11:16]))
            norm_values["gifs"].append(float(lines[4][11:16]))
            norm_values["throughput"].append(float(lines[8][12:18]))

    return norm_values


def gen_barplot():
    # Arrays with measured values.
    norm_values = load_results()

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
    ax = plt.gca()
    ax.tick_params(axis="both", which="major", pad=0)
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    # Save and show plot.
    plt.savefig(f"figures/{results_folder}_{'-'.join(versions)}")
    plt.show()


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

    # # Generate normalized bar plot with the given versions.
    # gen_barplot()

    # Generate throughput plot with the given versions.
    gen_throughput()
