from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


def load_data_sums():
    """Load data manually from Likwid results, taking the SUM columns of the STAT."""
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
    rows.append({"nthreads": 1, "type": "L2_request_rate", "value": 0.006429938})
    rows.append({"nthreads": 1, "type": "L2_request_rate", "value": 0.006461599})
    rows.append({"nthreads": 1, "type": "L2_request_rate", "value": 0.006424548})

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
    rows.append({"nthreads": 2, "type": "L2_request_rate", "value": 0.012945175})
    rows.append({"nthreads": 2, "type": "L2_request_rate", "value": 0.01291364})
    rows.append({"nthreads": 2, "type": "L2_request_rate", "value": 0.012964993})

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
    rows.append({"nthreads": 4, "type": "L2_request_rate", "value": 0.024248548})
    rows.append({"nthreads": 4, "type": "L2_request_rate", "value": 0.024273942})
    rows.append({"nthreads": 4, "type": "L2_request_rate", "value": 0.024431015})

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
    rows.append({"nthreads": 8, "type": "L2_request_rate", "value": 0.043094863})
    rows.append({"nthreads": 8, "type": "L2_request_rate", "value": 0.043285278})
    rows.append({"nthreads": 8, "type": "L2_request_rate", "value": 0.042908756})

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
    rows.append({"nthreads": 9, "type": "L2_request_rate", "value": 0.053153218})
    rows.append({"nthreads": 9, "type": "L2_request_rate", "value": 0.052998239})
    rows.append({"nthreads": 9, "type": "L2_request_rate", "value": 0.052567259})

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
    rows.append({"nthreads": 16, "type": "L2_request_rate", "value": 0.083510598})
    rows.append({"nthreads": 16, "type": "L2_request_rate", "value": 0.083945513})
    rows.append({"nthreads": 16, "type": "L2_request_rate", "value": 0.083138045})

    return pd.DataFrame(rows)


def load_data_gif_core():
    """Load data manually from Likwid results, taking the core with most instructions retired."""
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
    rows.append({"nthreads": 1, "type": "L2_miss_ratio", "value": 0.2588456})
    rows.append({"nthreads": 1, "type": "L2_miss_ratio", "value": 0.2584975})
    rows.append({"nthreads": 1, "type": "L2_miss_ratio", "value": 0.2597523})
    rows.append({"nthreads": 1, "type": "L2_request_rate", "value": 0.006429938})
    rows.append({"nthreads": 1, "type": "L2_request_rate", "value": 0.006461599})
    rows.append({"nthreads": 1, "type": "L2_request_rate", "value": 0.006424548})

    # 2 threads.
    rows.append({"nthreads": 2, "type": "L2_TRANS_ALL_REQUESTS", "value": 145097163})
    rows.append({"nthreads": 2, "type": "L2_TRANS_ALL_REQUESTS", "value": 144584126})
    rows.append({"nthreads": 2, "type": "L2_TRANS_ALL_REQUESTS", "value": 145310936})
    rows.append({"nthreads": 2, "type": "L2_RQSTS_MISS", "value": 34851218})
    rows.append({"nthreads": 2, "type": "L2_RQSTS_MISS", "value": 34882225})
    rows.append({"nthreads": 2, "type": "L2_RQSTS_MISS", "value": 34884865})
    rows.append({"nthreads": 2, "type": "L2_miss_rate", "value": 0.002004894})
    rows.append({"nthreads": 2, "type": "L2_miss_rate", "value": 0.002006672})
    rows.append({"nthreads": 2, "type": "L2_miss_rate", "value": 0.002006824})
    rows.append({"nthreads": 2, "type": "L2_miss_ratio", "value": 0.2666415})
    rows.append({"nthreads": 2, "type": "L2_miss_ratio", "value": 0.2412590})
    rows.append({"nthreads": 2, "type": "L2_miss_ratio", "value": 0.2006824})
    rows.append({"nthreads": 2, "type": "L2_request_rate", "value": 0.008347039})
    rows.append({"nthreads": 2, "type": "L2_request_rate", "value": 0.008317502})
    rows.append({"nthreads": 2, "type": "L2_request_rate", "value": 0.008359314})

    # 4 threads.
    rows.append({"nthreads": 4, "type": "L2_TRANS_ALL_REQUESTS", "value": 119294626})
    rows.append({"nthreads": 4, "type": "L2_TRANS_ALL_REQUESTS", "value": 119325553})
    rows.append({"nthreads": 4, "type": "L2_TRANS_ALL_REQUESTS", "value": 120812223})
    rows.append({"nthreads": 4, "type": "L2_RQSTS_MISS", "value": 27089421})
    rows.append({"nthreads": 4, "type": "L2_RQSTS_MISS", "value": 27119883})
    rows.append({"nthreads": 4, "type": "L2_RQSTS_MISS", "value": 27074122})
    rows.append({"nthreads": 4, "type": "L2_miss_rate", "value": 0.002473464})
    rows.append({"nthreads": 4, "type": "L2_miss_rate", "value": 0.002476260})
    rows.append({"nthreads": 4, "type": "L2_miss_rate", "value": 0.002472067})
    rows.append({"nthreads": 4, "type": "L2_miss_ratio", "value": 0.2270800})
    rows.append({"nthreads": 4, "type": "L2_miss_ratio", "value": 0.2272764})
    rows.append({"nthreads": 4, "type": "L2_miss_ratio", "value": 0.2241009})
    rows.append({"nthreads": 4, "type": "L2_request_rate", "value": 0.01089248})
    rows.append({"nthreads": 4, "type": "L2_request_rate", "value": 0.01089537})
    rows.append({"nthreads": 4, "type": "L2_request_rate", "value": 0.01103105})

    # 8 threads.
    rows.append({"nthreads": 8, "type": "L2_TRANS_ALL_REQUESTS", "value": 103145488})
    rows.append({"nthreads": 8, "type": "L2_TRANS_ALL_REQUESTS", "value": 103784012})
    rows.append({"nthreads": 8, "type": "L2_TRANS_ALL_REQUESTS", "value": 101774666})
    rows.append({"nthreads": 8, "type": "L2_RQSTS_MISS", "value": 22912042})
    rows.append({"nthreads": 8, "type": "L2_RQSTS_MISS", "value": 22912141})
    rows.append({"nthreads": 8, "type": "L2_RQSTS_MISS", "value": 22821783})
    rows.append({"nthreads": 8, "type": "L2_miss_rate", "value": 0.002966490})
    rows.append({"nthreads": 8, "type": "L2_miss_rate", "value": 0.002966504})
    rows.append({"nthreads": 8, "type": "L2_miss_rate", "value": 0.002954805})
    rows.append({"nthreads": 8, "type": "L2_miss_ratio", "value": 0.2221332})
    rows.append({"nthreads": 8, "type": "L2_miss_ratio", "value": 0.2207675})
    rows.append({"nthreads": 8, "type": "L2_miss_ratio", "value": 0.2242383})
    rows.append({"nthreads": 8, "type": "L2_request_rate", "value": 0.01335455})
    rows.append({"nthreads": 8, "type": "L2_request_rate", "value": 0.01343723})
    rows.append({"nthreads": 8, "type": "L2_request_rate", "value": 0.01317707})

    # 9 threads.
    rows.append({"nthreads": 9, "type": "L2_TRANS_ALL_REQUESTS", "value": 108537837})
    rows.append({"nthreads": 9, "type": "L2_TRANS_ALL_REQUESTS", "value": 107690352})
    rows.append({"nthreads": 9, "type": "L2_TRANS_ALL_REQUESTS", "value": 105506646})
    rows.append({"nthreads": 9, "type": "L2_RQSTS_MISS", "value": 22367536})
    rows.append({"nthreads": 9, "type": "L2_RQSTS_MISS", "value": 22371510})
    rows.append({"nthreads": 9, "type": "L2_RQSTS_MISS", "value": 22302367})
    rows.append({"nthreads": 9, "type": "L2_miss_rate", "value": 0.003038231})
    rows.append({"nthreads": 9, "type": "L2_miss_rate", "value": 0.003038772})
    rows.append({"nthreads": 9, "type": "L2_miss_rate", "value": 0.003029381})
    rows.append({"nthreads": 9, "type": "L2_miss_ratio", "value": 0.2060805})
    rows.append({"nthreads": 9, "type": "L2_miss_ratio", "value": 0.2077392})
    rows.append({"nthreads": 9, "type": "L2_miss_ratio", "value": 0.2113835})
    rows.append({"nthreads": 9, "type": "L2_request_rate", "value": 0.01474293})
    rows.append({"nthreads": 9, "type": "L2_request_rate", "value": 0.01462782})
    rows.append({"nthreads": 9, "type": "L2_request_rate", "value": 0.01433121})

    # 16 threads.
    rows.append({"nthreads": 16, "type": "L2_TRANS_ALL_REQUESTS", "value": 97071355})
    rows.append({"nthreads": 16, "type": "L2_TRANS_ALL_REQUESTS", "value": 98837923})
    rows.append({"nthreads": 16, "type": "L2_TRANS_ALL_REQUESTS", "value": 97130796})
    rows.append({"nthreads": 16, "type": "L2_RQSTS_MISS", "value": 20910072})
    rows.append({"nthreads": 16, "type": "L2_RQSTS_MISS", "value": 20804818})
    rows.append({"nthreads": 16, "type": "L2_RQSTS_MISS", "value": 20795623})
    rows.append({"nthreads": 16, "type": "L2_miss_rate", "value": 0.003415077})
    rows.append({"nthreads": 16, "type": "L2_miss_rate", "value": 0.003397888})
    rows.append({"nthreads": 16, "type": "L2_miss_rate", "value": 0.003396387})
    rows.append({"nthreads": 16, "type": "L2_miss_ratio", "value": 0.2154093})
    rows.append({"nthreads": 16, "type": "L2_miss_ratio", "value": 0.2104943})
    rows.append({"nthreads": 16, "type": "L2_miss_ratio", "value": 0.2140992})
    rows.append({"nthreads": 16, "type": "L2_request_rate", "value": 0.01585390})
    rows.append({"nthreads": 16, "type": "L2_request_rate", "value": 0.01614242})
    rows.append({"nthreads": 16, "type": "L2_request_rate", "value": 0.01586362})

    return pd.DataFrame(rows)


def plot_sums():
    """Loads and prints the SUM columns of the STATS."""
    # Manually add data from Likwid results.
    df = load_data_sums()

    # Take mean values of the collected resutls.
    df_mean = df.pivot_table(index="nthreads",
                             columns="type",
                             values="value",
                             aggfunc="mean")

    # Plot means of two lines, sharing one legend.
    sns.set(style="white")
    ax = df_mean[["L2_RQSTS_MISS"]].plot(figsize=(9, 6), rot=0, color="b",
                                         marker=".", legend=False)
    ax2 = ax.twinx()
    df_mean[["L2_TRANS_ALL_REQUESTS"]].plot(rot=0, ax=ax2, color="r", marker=".",
                                            legend=False)

    # Color ticks accordingly.
    ax.tick_params(axis='y', colors='b')
    ax2.tick_params(axis='y', colors='r')

    # Add title, labels, and legend.
    plt.title(f"L2 cache performance counters for v5.0", fontsize=16)
    ax.set_xlabel("Number of threads")
    ax.set_ylabel("Number of L2 misses")
    ax2.set_ylabel("Rate of L2 requests")

    ax.figure.legend()
    plt.show()


def plot_gif_core():
    """Loads and prints the SUM columns of the STATS."""
    # Manually add data from Likwid results.
    df = load_data_gif_core()

    # Take mean values of the collected resutls.
    df_mean = df.pivot_table(index="nthreads",
                             columns="type",
                             values="value",
                             aggfunc="mean")

    # Plot means of two lines, sharing one legend.
    sns.set(style="white")
    ax = df_mean[["L2_TRANS_ALL_REQUESTS"]].plot(figsize=(9, 6), rot=0, color="b",
                                                 marker=".", legend=False)
    ax2 = ax.twinx()
    df_mean[["L2_miss_rate"]].plot(rot=0, ax=ax2, color="r", marker=".",
                                   legend=False)

    # Color ticks accordingly.
    ax.tick_params(axis='y', colors='b')
    ax2.tick_params(axis='y', colors='r')

    # Add title, labels, and legend.
    plt.title(f"L2 cache performance counters for v5.0", fontsize=16)
    ax.set_xlabel("Number of threads")
    ax.set_ylabel("Number of L2 requests")
    ax2.set_ylabel("Rate of L2 misses")

    ax.figure.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plot_gif_core()
