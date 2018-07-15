#encoding: utf-8
from package import Package
from simulator import Simulator
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default = False)
    parser.add_argument('-utilization', type=float, default = 0)
    args = parser.parse_args()

    if(args.utilization == 0):
        utilization = 0
        for i in range(7):
            utilization += 0.1
            print("=================")
            print("Utilização ", utilization)
            print("=================")
            sim = Simulator(utilization, args.debug)
            sim.simulate()
    else:
        print("=================")
        print("Utilização ", args.utilization)
        print("=================")
        sim = Simulator(args.utilization,  args.debug)
        sim.simulate()

main()