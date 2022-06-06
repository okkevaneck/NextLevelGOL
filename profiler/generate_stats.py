"""
Generate CSV files with mean values and percentages.
"""
import pandas as pd
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

                # Error on empty.
                if len(lines) == 0:
                    print(f"Detected empty results file: {run_fp}..")
                    exit(1)

                rows.append({"version": v, "type": "init", "value": float(lines[1][12:17])})
                rows.append({"version": v, "type": "wrap", "value": float(lines[2][12:17])})
                rows.append({"version": v, "type": "step", "value": float(lines[3][12:17])})
                rows.append({"version": v, "type": "swap", "value": float(lines[4][12:17])})
                rows.append({"version": v, "type": "gif", "value": float(lines[5][12:17])})
                rows.append({"version": v, "type": "final", "value": float(lines[6][12:17])})

                # For pthreads code, we take the actual time as total, which makes the throughput 1 row lower.
                # Including version 7.0, because it is special (and does have latency hiding without pthreads).
                if (results_folder[:8] == "profiler" and int(v[1:2]) >= 6) \
                        or (results_folder[:7] == "scaling" and int(results_folder[9:10]) >= 6):
                    rows.append({"version": v, "type": "total", "value": float(lines[9][11:16])})
                    rows.append({"version": v, "type": "throughput", "value": float(lines[11][12:21])})
                else:
                    rows.append({"version": v, "type": "total", "value": float(lines[8][11:16])})
                    rows.append({"version": v, "type": "throughput", "value": float(lines[10][12:21])})

    values = pd.DataFrame(rows)

    return values


def gen_stats():
    # Fetch DatFrame with measured values.
    df = load_results()

    df_mean = None

    # If results are from profiler, just make a mean DataFrame.
    if results_folder[:8] == "profiler":
        # Create DataFrame with mean values and normalize.
        df_mean = df.pivot_table(index="version",
                                 columns="type",
                                 values="value",
                                 aggfunc="mean")
    # If results are from scaler, rename version column and transform to integer type.
    elif results_folder[:7] == "scaling":
        df = df.rename(columns={"version": "nthreads"})
        df = df.astype({'nthreads': 'int'})
        df_mean = df.pivot_table(index="nthreads",
                                 columns="type",
                                 values="value",
                                 aggfunc="mean")

    # Order DataFrame to plot in order.
    cols = ["throughput", "total", "final", "gif", "swap", "step", "wrap", "init"]
    df_mean = df_mean[cols]

    # Normalize the mean values to be between 0 and 1.
    df_mean_norm = df_mean.copy()
    df_mean_norm.iloc[:, 2:] = df_mean_norm.iloc[:, 2:].div(df_mean_norm.iloc[:, 2:].sum(axis=1), axis=0)

    # Write means file.
    with open(f"results/stats/{results_folder}_means.csv", "w") as fp:
        df_mean.to_csv(fp)

    # Write fractions file.
    with open(f"results/stats/{results_folder}_fractions.csv", "w") as fp:
        df_mean_norm.to_csv(fp)

    # Write percentage file.
    with open(f"results/stats/{results_folder}_percentages.csv", "w") as fp:
        df_mean_norm.multiply(100).to_csv(fp)


if __name__ == "__main__":
    # Get results folder and versions from command line.
    args = sys.argv
    results_folder = args[1]
    versions = args[2:]

    if versions[0] == "all":
        if results_folder[:8] == "profiler":
            versions = ["v0", "v1", "v2", "v3", "v4", "v5.0", "v5.1", "v6.0", "v6.1", "v7.0", "v7.1"]
        elif results_folder[:7] == "scaling":
            versions = ["1", "2", "4", "8", "9", "16"]

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
    gen_stats()
