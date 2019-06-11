##################
#   LIBRAIRIES   #
##################

from argparse import ArgumentParser
from random import randrange
import sys

##################
#   FUNCTIONS    #
##################

def get_arguments ():
    parser = ArgumentParser(description='Data generator program.')
    parser.add_argument('-w', '--weight',       type=float, help='weight')
    parser.add_argument('-b', '--biais',        type=float, help='biais')
    parser.add_argument('-i', '--individuals',  type=int,   help='nb individuals')

    res = parser.parse_args(sys.argv[1:])
    if res.individuals > 100000 or res.individuals <= 0:
        raise ValueError("Number of points must be an integer between 1 and 100000")
    return (res.individuals, res.weight, res.biais)

def main():
    data_file = "Data/datag.csv"
    try:
        nb_inds, weight, biais = get_arguments ()
    except Exception as e:
        print ("Error in arguments: {}".format(e))
        sys.exit(-1)

    try:
        open(data_file, "w")
    except Exception as e:
        print("Error: cannot open {} in write mode ({})".format(data_file, e))
        sys.exit(-1)
    
    try:
        with open(data_file, "w") as out_file:
            out_file.write("km,price\n")
            rand_num = 0
            rand_y = 0
            for i in range(nb_inds):
                rand_num = randrange(1, 250000)
                tmp = 0 * weight + biais
                base_line = rand_num * weight + biais
                tm = abs(int(float(tmp) * 0.1))
                if tm <= 1:
                    tm += 2
                rand_y = base_line + (randrange(1, tm * 2)) - randrange(1, tm)
                out_file.write("{},{}\n".format(rand_num, rand_y))
    except Exception as e:
        print("Error while generating data ({})".format(e))
        sys.exit(-1)

if __name__ == "__main__":
    main()