##################
#   LIBRAIRIES   #
##################

from vaex import open as vx_open
from argparse import ArgumentParser
import sys

##################
#   FUNCTIONS    #
##################


def get_arguments():
	parser = ArgumentParser(description='Data generator program.')
	parser.add_argument('-m', '--mileage', type=int, help='mileage', required=True)
	res = parser.parse_args(sys.argv[1:])
	if float(res.mileage) < 0.0 or float(res.mileage) > 250000.0:
		raise ValueError("Incorrect mileage (values must be between 0 and 250000)")
	return (res.mileage)

def main():
	try:
		mileage = get_arguments()
	except Exception as e:
		print ("Error in arguments: {}".format(e))
		sys_exit(-1)

	try:
		df = vx_open("Models/weights.csv")
		res = float(df['biais'].values[0]) + float(mileage) * float(df['weight'].values[0])
		print("The given price for {} mile(s) is :\n{}".format(mileage, res))
	except Exception as e:
		print(e)

if __name__ == "__main__":
    main()
