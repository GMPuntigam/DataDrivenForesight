import matplotlib.ticker as mtick
import matplotlib.transforms as transforms
import pandas as pd
import matplotlib.pyplot as plt

def butterfly_chart(
        data: pd.DataFrame, 
        title: str = None,
        middle_label_offset=0.00,
        figsize=(5, 2),
        wspace=0.6
    ):

    fig, (ax1, ax2) = plt.subplots(
        figsize=figsize,
        dpi=100,
        nrows=1,
        ncols=2,
        subplot_kw={'yticks': []},
        gridspec_kw={'wspace': wspace},
    )
    plt.subplots_adjust(left=0.01, right=0.99)
    # plot the data
    (l1, x1), (l2,x2) = data.items()
    y = range(len(x1))
    labels = data.index.tolist()

    bars = ax1.barh(y=y, width=x1, color='tab:blue', zorder=3)
    
    ax1.invert_xaxis()
    ax1.set_title(l1)
    ax1.grid(which='major', axis='x', linestyle='-')
    ax1.set_axisbelow(True)
    bars2 = ax2.barh(y=y, width=x2, color='tab:blue', zorder=3)
    for bar, label in zip(bars2, labels):
        if label == "INDIA":
            bar.set_color('red')
        if label in ["BELGIUM","NETHERLANDS","SINGAPORE"]:
            bar.set_color('coral')
    ax2.set_title(l2)
    ax2.grid(which='major', axis='x', linestyle='-')
    ax2.set_axisbelow(True)
    # turn on axes spines on the inside y-axis
    ax1.spines['right'].set_visible(True)
    ax2.spines['left'].set_visible(True)
    
    # format axes
    # xfmt = mtick.PercentFormatter(xmax=1, decimals=0)
    # ax1.xaxis.set_major_formatter(xfmt)
    # ax2.xaxis.set_major_formatter(xfmt)

    # place center labels
    transform = transforms.blended_transform_factory(fig.transFigure, ax1.transData)
    for i, label in enumerate(labels):
        ax1.text(0.5+middle_label_offset, i, label, ha='center', va='center', transform=transform)

    plt.suptitle(title, y=0.98, fontsize='x-large')