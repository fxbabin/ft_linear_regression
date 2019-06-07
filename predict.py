##################
#   LIBRAIRIES   #
##################

import vaex

##################
#   FUNCTIONS    #
##################

def main():
	df = vaex.open("Data/data.csv")
	weight = float(data.weight)
	bias = float(data.bias)
	mileage = input("Please enter a mileage : ")
	prediction = tf.add(tf.multiply(weight, float(mileage)), bias)

	with tf.Session() as sess:
		result = sess.run(prediction)
		print("This car is worth : {} euro(s)".format(result))

if __name__ == "__main__":
	main()
