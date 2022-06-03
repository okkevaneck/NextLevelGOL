"""
Generate figures for scaling plots.
"""
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import os
import glob


def load_results():
    rows = []

    # Load results in variables.
    for t in threads:
        fs = glob.glob(f"results/{results_folder}/{t}_*")
        v = results_folder[9:12]

        for run_fp in fs:
            with open(run_fp, "r") as fp:
                lines = fp.readlines()

                # Skip empty.
                if len(lines) == 0:
                    print(f"Detected empty results file: {run_fp}..")
                    exit(1)

                rows.append({"nthreads": int(t), "type": "init", "value": float(lines[1][12:17])})
                rows.append({"nthreads": int(t), "type": "wrap", "value": float(lines[2][12:17])})
                rows.append({"nthreads": int(t), "type": "step", "value": float(lines[3][12:17])})
                rows.append({"nthreads": int(t), "type": "swap", "value": float(lines[4][12:17])})
                rows.append({"nthreads": int(t), "type": "gif", "value": float(lines[5][12:17])})
                rows.append({"nthreads": int(t), "type": "final", "value": float(lines[6][12:17])})

                # For pthreads code, we take the actual time as total, which makes the throughput 1 row lower.
                # Including version 7.0, because it is special (and does have latency hiding without pthreads).
                if int(v[0]) >= 6:
                    rows.append({"nthreads": int(t), "type": "total", "value": float(lines[9][11:16])})
                    rows.append({"nthreads": int(t), "type": "throughput", "value": float(lines[11][12:18])})
                    rows.append({"nthreads": int(t), "type": "overlap",
                                 "value": float(lines[8][12:18]) - float(lines[9][12:18])})
                else:
                    rows.append({"nthreads": int(t), "type": "total", "value": float(lines[8][11:16])})
                    rows.append({"nthreads": int(t), "type": "throughput", "value": float(lines[10][12:18])})
                    rows.append({"nthreads": int(t), "type": "overlap", "value": 0.0})

    values = pd.DataFrame(rows)

    return values


def gen_scaling_plot():
    # Fetch DatFrame with measured values.
    df = load_results()

    # Create DataFrame with mean values and normalize.
    df_mean = df.pivot_table(index="nthreads",
                             columns="type",
                             values="value",
                             aggfunc="mean")

    cols = ["throughput", "total", "final",  "swap", "gif", "overlap", "step", "wrap", "init"]
    df_mean = df_mean[cols]

    # Subtract overlap of step for all rows that do not belong to v7.0.
    # Subtract overlap of gif for the rows of version 7.0.
    idxs = list(df_mean.index)

    if "v7.0" in idxs:
        idxs.remove("v7.0")
        df_mean.loc[["v7.0"]]["step"] -= df_mean.loc[["v7.0"]]["overlap"]

    df_mean.loc[idxs]["step"] -= df_mean.loc[idxs]["overlap"]

    # Create DataFrame for the error bars (std).
    df_std = df.pivot_table(index="nthreads",
                            columns="type",
                            values="value",
                            aggfunc="std")

    # Plot means.
    sns.set(style="white")
    ax = df_mean[cols[2:]].plot(kind="bar", stacked=True, figsize=(9, 6), rot=0,
                                # yerr=df_std[["step", "gif", "final"]]
                                )

    # Color hatches properly.
    mpl.rcParams["hatch.linewidth"] = 7.5
    edgeColor = None

    for i in range(len(threads)):
        ovlpIdx = len(threads) * cols[2:].index("overlap") + i
        ax.patches[ovlpIdx].set_hatch("/")

        if edgeColor is None:
            edgeColor = ax.patches[ovlpIdx - 1].get_facecolor()

        ax.patches[ovlpIdx].set_edgecolor(edgeColor)

    # Recolor all bars above hatch.
    for i in range(len(threads)):
        ovlpIdx = len(threads) * cols[2:].index("overlap") + i
        stepIdx = len(threads) * cols[2:].index("step") + i
        wrapIdx = len(threads) * cols[2:].index("wrap") + i
        initIdx = len(threads) * cols[2:].index("init") + i

        ax.patches[initIdx].set_facecolor(ax.patches[wrapIdx].get_facecolor())
        ax.patches[wrapIdx].set_facecolor(ax.patches[stepIdx].get_facecolor())
        ax.patches[stepIdx].set_facecolor(ax.patches[ovlpIdx].get_facecolor())


    # Add info to plot.
    plt.title("Time spend per number of threads", fontsize=16)
    plt.xlabel("Number of threads", labelpad=0)
    plt.ylabel("Time spend (s)")
    plt.xticks(rotation=0)
    ax = plt.gca()
    ax.tick_params(axis="both", which="major", pad=0)
    handles, labels = ax.get_legend_handles_labels()

    # Remove overlap from legend.
    handles.pop(labels.index("overlap"))
    labels.pop(labels.index("overlap"))
    ax.legend(handles[::-1], labels[::-1], loc="center left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    # Save and show plot.
    # plt.savefig(f"figures/{results_folder}_{'-'.join(threads)}.png")
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

    # Generate normalized bar plot with the given versions.
    gen_scaling_plot()
