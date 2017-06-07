import numpy as np
from numpy import vstack  # VSTACK((a,b)) stacks B on TOP of A
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import math
import argparse
import sys


def csv_to_numpy(csv_file):
    with open(csv_file, 'r') as infile:
        lines = infile.readlines()
    stack = None
    for line in lines:
        newline = []
        for x in [int(y) for y in line.split(',')]:
            if x <= 0:
                newline.append(0)
            else:
                newline.append(math.log(x,10))
        x = np.array(newline)
        if stack == None:
            stack = x
        else:
            try:
                stack = vstack((stack, x))  # Double (( )) on purpose
            except Exception as e:
                if False:
                    print 'Error: cannot vstack len:{}'.format(len(x))
    return stack

def sortNumpyStack(stack):
    stack = stack.tolist()
    stack.sort(key=sum, reverse=True)
    stack = np.array(stack)
    return stack


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This program finds the most conserved sequences from a directory of bamfiles and outputs them in fasta format')
    parser.add_argument('-i', help='The location of the CSV file to be made into a heatmap', required=True)
    parser.add_argument('-o', help='File name of the figure', required=True)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    csvArray = csv_to_numpy(args.i)
    ax = sns.heatmap(csvArray, xticklabels=[], yticklabels=[])
    # plt.show()  # Uncommenting this line will show the figure before saving
    plt.savefig(args.o)






