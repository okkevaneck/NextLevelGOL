"""
Generate figures for barplots.
"""
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
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
                # rows.append({"version": v, "type": "total", "value": float(lines[8][11:16])})
                # rows.append({"version": v, "type": "throughput", "value": float(lines[10][12:18])})

                # value = {"version": v,
                #          "init": float(lines[1][12:17]),
                #          "wrap": float(lines[2][12:17]),
                #          "step": float(lines[3][12:17]),
                #          "swap": float(lines[4][12:17]),
                #          "gif": float(lines[5][12:17]),
                #          "final": float(lines[6][12:17]),
                #          "total": float(lines[8][11:16]),
                #          "throughput": float(lines[10][12:18])}
                # rows.append(value)

    values = pd.DataFrame(rows)

    return values


def gen_barplot():
    # Arrays with measured values.
    df = load_results()

    # Make normalized DataFrame.
    # df = values.iloc[:, 1:7] = values.iloc[:, 1:7].div(values.iloc[:, 1:7].sum(axis=1), axis=0)
    print(df)

    # Create DataFrame with mean values.
    df_mean = df.pivot_table(index="version",
                            columns="type",
                            values="value",
                            aggfunc="mean")

    print(df_mean)

    # Create DataFrame for the error bars (std).
    df_std = df.pivot_table(index="version",
                            columns="type",
                            values="value",
                            aggfunc="std")
    print(df_std)

    # plot the dataframe and add yerr
    ax = df_mean.plot(kind="bar", stacked=True, figsize=(9, 6), rot=0, yerr=df_std)
    plt.show()

    # TODO: https://stackoverflow.com/questions/70333645/how-to-annotate-bar-plots-when-adding-error-bars

    #
    # # plot the dataframe and add yerr
    # ax = pen_mean.plot(kind='bar', stacked=True, figsize=(9, 6), rot=0, yerr=pen_std)

    # # Setup stacked barchart.
    # sns.set(style="white")
    # df.set_index("Version").plot(kind="bar", stacked=True)
    #
    # # Add info to plot.
    # plt.title("Relative time spend per version", fontsize=16)
    # plt.xlabel("Versions", labelpad=0)
    # plt.ylabel("Relative time spend")
    # plt.xticks(rotation=45)
    # ax = plt.gca()
    # ax.tick_params(axis="both", which="major", pad=0)
    # ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    # plt.tight_layout()
    #
    # # Save and show plot.
    # plt.savefig(f"figures/{results_folder}_{'-'.join(versions)}")
    # plt.show()


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
