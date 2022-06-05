from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


def load_data():
    """Load data manually from Likwid results."""
    rows = []

    # 1 thread.
    rows.append({"nthreads": 1, "type": "L2_TRANS_ALL_REQUESTS", "value": 194306777})
    rows.append({"nthreads": 1, "type": "L2_TRANS_ALL_REQUESTS", "value": 195263566})
    rows.append({"nthreads": 1, "type": "L2_TRANS_ALL_REQUESTS", "value": 194143900})
    rows.append({"nthreads": 1, "type": "L2_RQSTS_MISS", "value": 50295453})
    rows.append({"nthreads": 1, "type": "L2_RQSTS_MISS", "value": 50475134})
    rows.append({"nthreads": 1, "type": "L2_RQSTS_MISS", "value": 50429322})
    rows.append({"nthreads": 1, "type": "L2_miss_rate", "value": 0.001664361})
    rows.append({"nthreads": 1, "type": "L2_miss_rate", "value": 0.001670307})
    rows.append({"nthreads": 1, "type": "L2_miss_rate", "value": 0.001668791})

    # 2 threads.
    rows.append({"nthreads": 2, "type": "L2_TRANS_ALL_REQUESTS", "value": 204362790})
    rows.append({"nthreads": 2, "type": "L2_TRANS_ALL_REQUESTS", "value": 203823775})
    rows.append({"nthreads": 2, "type": "L2_TRANS_ALL_REQUESTS", "value": 204673559})
    rows.append({"nthreads": 2, "type": "L2_RQSTS_MISS", "value": 50653893})
    rows.append({"nthreads": 2, "type": "L2_RQSTS_MISS", "value": 50677239})
    rows.append({"nthreads": 2, "type": "L2_RQSTS_MISS", "value": 50679406})
    rows.append({"nthreads": 2, "type": "L2_miss_rate", "value": 0.003230948})
    rows.append({"nthreads": 2, "type": "L2_miss_rate", "value": 0.002006672})
    rows.append({"nthreads": 2, "type": "L2_miss_rate", "value": 0.002006824})

    # 4 threads.
    rows.append({"nthreads": 4, "type": "L2_TRANS_ALL_REQUESTS", "value": 205323103})
    rows.append({"nthreads": 4, "type": "L2_TRANS_ALL_REQUESTS", "value": 205499278})
    rows.append({"nthreads": 4, "type": "L2_TRANS_ALL_REQUESTS", "value": 207123465})
    rows.append({"nthreads": 4, "type": "L2_RQSTS_MISS", "value": 51058210})
    rows.append({"nthreads": 4, "type": "L2_RQSTS_MISS", "value": 51052730})
    rows.append({"nthreads": 4, "type": "L2_RQSTS_MISS", "value": 50966933})
    rows.append({"nthreads": 4, "type": "L2_miss_rate", "value": 0.006194665})
    rows.append({"nthreads": 4, "type": "L2_miss_rate", "value": 0.006191866})
    rows.append({"nthreads": 4, "type": "L2_miss_rate", "value": 0.006181466})

    # 8 threads.
    rows.append({"nthreads": 8, "type": "L2_TRANS_ALL_REQUESTS", "value": 198986917})
    rows.append({"nthreads": 8, "type": "L2_TRANS_ALL_REQUESTS", "value": 199972269})
    rows.append({"nthreads": 8, "type": "L2_TRANS_ALL_REQUESTS", "value": 197587174})
    rows.append({"nthreads": 8, "type": "L2_RQSTS_MISS", "value": 50581850})
    rows.append({"nthreads": 8, "type": "L2_RQSTS_MISS", "value": 50556316})
    rows.append({"nthreads": 8, "type": "L2_RQSTS_MISS", "value": 50472848})
    rows.append({"nthreads": 8, "type": "L2_miss_rate", "value": 0.01155276})
    rows.append({"nthreads": 8, "type": "L2_miss_rate", "value": 0.011544719})
    rows.append({"nthreads": 8, "type": "L2_miss_rate", "value": 0.011535204})

    # 9 threads.
    rows.append({"nthreads": 9, "type": "L2_TRANS_ALL_REQUESTS", "value": 218591478})
    rows.append({"nthreads": 9, "type": "L2_TRANS_ALL_REQUESTS", "value": 217629228})
    rows.append({"nthreads": 9, "type": "L2_TRANS_ALL_REQUESTS", "value": 215060849})
    rows.append({"nthreads": 9, "type": "L2_RQSTS_MISS", "value": 51312043})
    rows.append({"nthreads": 9, "type": "L2_RQSTS_MISS", "value": 51429281})
    rows.append({"nthreads": 9, "type": "L2_RQSTS_MISS", "value": 51264781})
    rows.append({"nthreads": 9, "type": "L2_miss_rate", "value": 0.013140276})
    rows.append({"nthreads": 9, "type": "L2_miss_rate", "value": 0.013180369})
    rows.append({"nthreads": 9, "type": "L2_miss_rate", "value": 0.013137671})

    # 16 threads.
    rows.append({"nthreads": 16, "type": "L2_TRANS_ALL_REQUESTS", "value": 206059767})
    rows.append({"nthreads": 16, "type": "L2_TRANS_ALL_REQUESTS", "value": 208140955})
    rows.append({"nthreads": 16, "type": "L2_TRANS_ALL_REQUESTS", "value": 205502125})
    rows.append({"nthreads": 16, "type": "L2_RQSTS_MISS", "value": 51958275})
    rows.append({"nthreads": 16, "type": "L2_RQSTS_MISS", "value": 51715545})
    rows.append({"nthreads": 16, "type": "L2_RQSTS_MISS", "value": 51171782})
    rows.append({"nthreads": 16, "type": "L2_miss_rate", "value": 0.022683444})
    rows.append({"nthreads": 16, "type": "L2_miss_rate", "value": 0.022566203})
    rows.append({"nthreads": 16, "type": "L2_miss_rate", "value": 0.022248411})

    return pd.DataFrame(rows)


if __name__ == '__main__':
    # Manually add data from Likwid results.
    df = load_data()

    # Take mean values of the collected resutls.
    df_mean = df.pivot_table(index="nthreads",
                             columns="type",
                             values="value",
                             aggfunc="mean")

    print(df_mean)

    # Plot means.
    sns.set(style="white")
    ax = df_mean[["L2_RQSTS_MISS"]].plot(figsize=(9, 6), rot=0)
    plt.show()
