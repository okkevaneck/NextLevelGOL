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
#     values = {
#         "inits": [],
#         "wraps": [],
#         "steps": [],
#         "swaps": [],
#         "gifs": [],
#         "finals": [],
#         "throughput": [],
#     }
#
#     # Load results in variables.
# for t in threads:
#     fs = glob.glob(f"results/{results_folder}/{t}_*")
#     with open(fs[0], "r") as fp:
#         lines = fp.readlines()
#
#         values["inits"].append(float(lines[1][11:16]))
#         values["wraps"].append(float(lines[2][11:16]))
#         values["steps"].append(float(lines[3][11:16]))
#         values["swaps"].append(float(lines[4][11:16]))
#         values["gifs"].append(float(lines[5][11:16]))
#         values["finals"].append(float(lines[6][11:16]))
#         values["throughput"].append(float(lines[10][12:18]))
#
# return values
#
#
    rows = []

    # Load results in variables.
    for t in threads:
        fs = glob.glob(f"results/{results_folder}/{t}_*")

        for run_fp in fs:
            with open(run_fp, "r") as fp:
                lines = fp.readlines()

                # Skip empty.
                if len(lines) == 0:
                    continue

                rows.append({"nthreads": t, "type": "init", "value": float(lines[1][12:17])})
                rows.append({"nthreads": t, "type": "wrap", "value": float(lines[2][12:17])})
                rows.append({"nthreads": t, "type": "step", "value": float(lines[3][12:17])})
                rows.append({"nthreads": t, "type": "swap", "value": float(lines[4][12:17])})
                rows.append({"nthreads": t, "type": "gif", "value": float(lines[5][12:17])})
                rows.append({"nthreads": t, "type": "final", "value": float(lines[6][12:17])})

                # For pthreads code, we take the actual time as total, which makes the throughput 1 row lower.
                # Including version 7.0, because it is special (and does have latency hiding without pthreads).
                if int(v[1:2]) >= 6:
                    rows.append({"nthreads": t, "type": "total", "value": float(lines[9][11:16])})
                    rows.append({"nthreads": t, "type": "throughput", "value": float(lines[11][12:18])})
                else:
                    rows.append({"nthreads": t, "type": "total", "value": float(lines[8][11:16])})
                    rows.append({"nthreads": t, "type": "throughput", "value": float(lines[10][12:18])})

    values = pd.DataFrame(rows)

    return values


def gen_scaling_plot():
    # Fetch DatFrame with measured values.
    df = load_results()

    # Create DataFrame with mean values and normalize.
    df_mean = df.pivot_table(index="version",
                             columns="type",
                             values="value",
                             aggfunc="mean")

    # # Order DataFrame to plot in order.
    # cols = ["throughput", "total", "final", "gif", "swap", "step", "wrap", "init"]
    # df_mean = df_mean[cols]

    # Create DataFrame with normalized performance numbers.
    df = pd.DataFrame({"nthreads": threads,
                       "init": df_mean["init"],
                       "wrap": df_mean["wraps"],
                       "step": df_mean["steps"],
                       "swap": df_mean["swaps"],
                       "gif":  df_mean["gifs"],
                       "final":  df_mean["final"]})

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
