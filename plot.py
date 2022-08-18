import json
import argparse
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def main():

    # parse the input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='number of photos')
    parser.add_argument('m', type=int, help='number of modes')
    parser.add_argument('n_param', type=int, help='number of beam-spliters')
    parser.add_argument('v', type=int, help='version of the architecture')
    parser.add_argument('filename', type=str, help='the name of the json file')
    parser.add_argument('outputfile', type=str, help='path to the output file')
    args = parser.parse_args()

    directory = "data/n{}_m{}_nparam{}_v{}/".format(args.n, args.m, args.n_param, args.v)
    # relative path to the json file and
    # relative path to the image file
    input_path = directory + args.filename
    output_path = directory + args.outputfile

    # load the json file containing the probabilities
    with open(input_path, "r") as f:
        res = json.load(f)
    
    # x-axis is either the fock states or the binary strings
    # y-axis is the associated probabilities
    x = list(res.keys())
    y = list(res.values())

    # bar plot of the probabilities
    fig = plt.figure(figsize=(16, 8))
    ax = fig.add_subplot(111)
    ax.bar(x, y)
    ticks_loc = list(ax.get_xticks())
    ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    ax.set_xticklabels(x, rotation = 90)
    ax.set_ylabel("Probability")
    if "simulation" in args.filename:
        ax.set_xlabel("Binary Strings")
    else:
        ax.set_xlabel("Fock States")
    plt.savefig(output_path)
    plt.close(fig)

if __name__ == "__main__":
    main()