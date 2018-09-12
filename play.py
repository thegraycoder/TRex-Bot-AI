from trex import TRex


def main():
    trex = TRex()
    while True:
        trex.execute()
        trex.keep_best_genomes()
        trex.mutations()


if __name__ == '__main__':
    main()
