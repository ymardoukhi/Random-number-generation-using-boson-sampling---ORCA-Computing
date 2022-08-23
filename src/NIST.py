import pandas as pd
import matplotlib.pyplot as plt

def nist_plot(n: int, m: int, param: int, v: int, protocol: str) -> None:
    """
    function that plots the p-value of the 
    NIST statistical test suit for various tests.

    input:
        n (int): number of photos
        m (int): number of modes
        param (int): number of parameters
        v (int): version
        protocal (str): can be either vonneumann, huffman or permutation
    return:
        _ (None): plots the bar plots of the p-value of the different NIST
            statistical tests
    """
    tests = ["SingleTests", "RandomExcursions", "CumulativeSums", "RandomExcursionsVariant", "NonOverlappingTemplate"]

    fig = plt.figure()
    spec = fig.add_gridspec(3, 2)

    for ind, test in enumerate(tests):
        data = pd.read_csv("data/n{}_m{}_nparam{}_v{}/nist/{}/{}.txt".format(n, m, param, v, protocol, test), delimiter="\t")

        if ind in [0, 1]:
            ax = fig.add_subplot(spec[0, ind%2])
            if (ind+1)%2:
                ax.set_ylabel("p-value")
        elif ind in [2, 3]:
            ax = fig.add_subplot(spec[1, ind%2])
            if (ind+1)%2:
                ax.set_ylabel("p-value")
        else:
            ax = fig.add_subplot(spec[2, :])
            ax.set_ylabel("p-value")

        ax.bar(data.index.to_list(), data["p-value"].to_list())
        if ind == 0:
            plt.xticks(data.index, data["test"].to_list(), rotation=45)
        else:
            ax.set_xticks([])
            ax.set_xticklabels([])
            ax.set_title(test)
        ax.hlines(y=0.01, xmin=0.0, xmax=len(data.index) ,linestyle='--', color="#9e2b3c")
    
    plt.tight_layout()
    plt.show()
    



