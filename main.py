#encoding: utf-8
from package import Package
from simulator import Simulator
import sys
import argparse
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default = False)
    parser.add_argument('--plot', action='store_true', default = False)
    parser.add_argument('-u', type=float, default = 0)
    args = parser.parse_args()

    t0 = time.time()

    if(args.u == 0):
        utilization = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
        for x in utilization:
            print("=================")
            print("Utilização ", x)
            print("=================")
            sim = Simulator(x, args.debug, args.plot)
            sim.simulate()
    else:
        print("=================")
        print("Utilização ", args.u)
        print("=================")
        sim = Simulator(args.u,  args.debug, args.plot)
        sim.simulate()

    t = time.time() - t0
    print("Total execution time: " + str(t))

main()