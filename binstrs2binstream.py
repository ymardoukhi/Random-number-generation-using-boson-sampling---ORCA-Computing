import os
import json
import argparse

def main():
    
    # parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='path to the input file')
    parser.add_argument('output', type=str, help='path to the output file')
    args = parser.parse_args()

    # set the data path to load the simulation results
    if not os.path.exists(args.input):
        raise FileNotFoundError("path {} does not exists".format(args.input))

    with open(args.input, "r") as f:
        strs = json.load(f)
    
    with open(args.output, "w") as f:
        f.write("".join(strs))


if __name__ == "__main__":
    main()
