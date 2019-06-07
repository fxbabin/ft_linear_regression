##################
#   LIBRAIRIES   #
##################

import vaex
import argparse
import sys

##################
#   FUNCTIONS    #
##################


def get_arguments():
    parser = argparse.ArgumentParser(description='Data generator program.')
    parser.add_argument('-m', '--mileage', help='mileage')
    res = parser.parse_args(sys.argv[1:])
    return (res.mileage)


def main():
	mileage = get_arguments()
	try:
		open("Models/weights.csv", "r")
	except Exception as e:
		print(e)
		sys.exit(-1)
	try:
		df = vaex.open("Models/weights.csv")
		print("The given price for {} mile(s) is :".format(mileage))
		print(float(df['biais'].values[0]) + float(mileage) * float(df['weight'].values[0]))
	except Exception as e:
		print(e)

if __name__ == "__main__":
    main()
