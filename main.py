from package import Package
from simulator import Simulator

def main():
    # a utilização1 vai variar de 0.1 até 0.7 em incrementos de 0.1
    # utilização1 = taxa * E[X1]
    # Nao entendi a utilização do pacote de voz
        
    sim = Simulator(0.10)
    sim.simulate()

main()