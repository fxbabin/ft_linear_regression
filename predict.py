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
    parser.add_argument('-m', '--mileage', help='mileage', required=True)
    res = parser.parse_args(sys.argv[1:])
    return (res.mileage)


def main():
	try:
		mileage = get_arguments()
		if float(mileage) < 0.0 :
			print("enter a positive mileage")
			sys.exit(-1)
		open("Models/weights.csv")
		df = vaex.open("Models/weights.csv")
		print("The given price for {} mile(s) is :".format(mileage))
		print(float(df['biais'].values[0]) + float(mileage) * float(df['weight'].values[0]))
	except Exception as e:
		print(e)

if __name__ == "__main__":
    main()
