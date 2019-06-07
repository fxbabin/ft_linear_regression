import argparse
import sys
import random

def get_arguments ():
    parser = argparse.ArgumentParser(description='Data generator program.')
    parser.add_argument('-w', '--weight', help='weight')
    parser.add_argument('-b', '--biais', help='biais')
    parser.add_argument('-i', '--individuals', help='nb individuals')

    res = parser.parse_args(sys.argv[1:])
    return (int(res.individuals), float(res.weight), float(res.biais))

def main():
    try:
        nb_inds, weight, biais = get_arguments ()
    except Exception as e:
        print ("Error in arguments: {}".format(e))
        sys.exit(-1)

    with open("Data/datag.csv", "w") as out_file:
        out_file.write("km,price\n")
        rand_num = 0
        rand_y = 0
        for i in range(nb_inds):
            rand_num = random.randrange(1, 250000)
            rand_y = rand_num * weight + biais - (random.randrange(1, 250000 * 0.1)) + (random.randrange(1, 250000 * 0.2))
            out_file.write("{},{}\n".format(rand_num, rand_y))

if __name__ == "__main__":
    main()