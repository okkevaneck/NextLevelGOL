"""
Generate figures for barplots.
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
    for v in versions:
        fs = glob.glob(f"results/{results_folder}/{v}_*.out")

        for run_fp in fs:
            with open(run_fp, "r") as fp:
                lines = fp.readlines()
                rows.append({"version": v, "type": "init", "value": float(lines[1][12:17])})
                rows.append({"version": v, "type": "wrap", "value": float(lines[2][12:17])})
                rows.append({"version": v, "type": "step", "value": float(lines[3][12:17])})
                rows.append({"version": v, "type": "swap", "value": float(lines[4][12:17])})
                rows.append({"version": v, "type": "gif", "value": float(lines[5][12:17])})
                rows.append({"version": v, "type": "final", "value": float(lines[6][12:17])})

                # For pthreads code, we take the actual time as total, which makes the throughput 1 row lower.
                # Including version 7.0, because it is special (and does have latency hiding without pthreads).
                if int(v[1:2]) >= 6:
                    rows.append({"version": v, "type": "total", "value": float(lines[9][11:16])})
                    rows.append({"version": v, "type": "throughput", "value": float(lines[11][12:21])})
                    rows.append({"version": v, "type": "overlap",
                                 "value": float(lines[8][12:18]) - float(lines[9][12:18])})
                else:
                    rows.append({"version": v, "type": "total", "value": float(lines[8][11:16])})
                    rows.append({"version": v, "type": "throughput", "value": float(lines[10][12:21])})
                    rows.append({"version": v, "type": "overlap", "value": 0.0})

    values = pd.DataFrame(rows)

    return values


def gen_barplot():
    # Fetch DatFrame with measured values.
    df = load_results()

    # Create DataFrame with mean values and normalize.
    df_mean = df.pivot_table(index="version",
                             columns="type",
                             values="value",
                             aggfunc="mean")

    # Order DataFrame to plot in order.
    cols = ["throughput", "total", "final",  "swap", "gif", "overlap", "step", "wrap", "init"]
    df_mean = df_mean[cols]

    # Subtract overlap of step for all rows that do not belong to v7.0.
    # Subtract overlap of gif for the rows of version 7.0.
    idxs = list(df_mean.index)

    if "v7.0" in idxs:
        idxs.remove("v7.0")
        df_mean.loc[["v7.0"]]["step"] -= df_mean.loc[["v7.0"]]["overlap"]

    df_mean.loc[idxs]["step"] -= df_mean.loc[idxs]["overlap"]

    # Normalize the mean values to be between 0 and 1.
    df_mean_norm = df_mean.copy()
    df_mean_norm.iloc[:, 2:] = df_mean_norm.iloc[:, 2:].div(df_mean_norm.iloc[:, 2:].sum(axis=1), axis=0)

    # Create DataFrame for the error bars (std).
    df_std = df.pivot_table(index="version",
                            columns="type",
                            values="value",
                            aggfunc="std")

    # Scale the standard deviation to be relative for the 0-1 scale.
    for i in range(len(df_std)):
        df_std.iloc[i][cols[2:]] = df_std.iloc[i][cols[2:]].divide(df_mean.iloc[i]['total'])

    # Plot the dataframe and add error bars.
    sns.set(style="white")
    ax = df_mean_norm[cols[2:]].plot(kind="bar", stacked=True, figsize=(9, 6), rot=0,
                                     # yerr=df_std[["step", "gif", "final"]],
                                     linewidth=0)

    # Color hatches properly.
    mpl.rcParams["hatch.linewidth"] = 7.5
    edgeColor = None

    for i in range(len(versions)):
        ovlpIdx = len(versions) * cols[2:].index("overlap") + i
        ax.patches[ovlpIdx].set_hatch("/")

        if edgeColor is None:
            edgeColor = ax.patches[ovlpIdx - 1].get_facecolor()

        ax.patches[ovlpIdx].set_edgecolor(edgeColor)

    # Recolor all bars above hatch.
    for i in range(len(versions)):
        ovlpIdx = len(versions) * cols[2:].index("overlap") + i
        stepIdx = len(versions) * cols[2:].index("step") + i
        wrapIdx = len(versions) * cols[2:].index("wrap") + i
        initIdx = len(versions) * cols[2:].index("init") + i

        ax.patches[initIdx].set_facecolor(ax.patches[wrapIdx].get_facecolor())
        ax.patches[wrapIdx].set_facecolor(ax.patches[stepIdx].get_facecolor())
        ax.patches[stepIdx].set_facecolor(ax.patches[ovlpIdx].get_facecolor())

    # Add info to plot.
    plt.title("Segregated execution time per version", fontsize=16)
    plt.title("Normalized segregated execution time per version", fontsize=16)
    plt.xlabel("Version", labelpad=0)
    plt.ylabel("Execution time (s)")
    plt.xticks(rotation=45)
    ax = plt.gca()
    ax.tick_params(axis="both", which="major", pad=0)
    handles, labels = ax.get_legend_handles_labels()

    # Remove overlap from legend.
    handles.pop(labels.index("overlap"))
    labels.pop(labels.index("overlap"))
    ax.legend(handles[::-1], labels[::-1], loc="center left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    # Save and show plot.
    # plt.savefig(f"figures/barplots_no_error/{results_folder}_{'-'.join(versions)}.png")
    plt.savefig(f"figures/barplots_norm_no_error/{results_folder}_{'-'.join(versions)}.png")
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
