##################
#   LIBRAIRIES   #
##################

import vaex
import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import argparse
from tqdm import tqdm

##################
#   FUNCTIONS    #
##################

def featureNormalize(X):
    x_min = X.min(axis=0)
    x_max = X.max(axis=0)
    X = (X - x_min)/ (x_max - x_min)
    return X, x_min, x_max

def predict(X, theta):
    return(np.dot(X, theta))

def cost(X, y, theta, lbda=0.0, regularization="L2"):
    reg = 0
    if regularization == "L1":
        reg = lbda * np.sum(np.absolute(theta))
    else:
        reg = lbda * np.dot(theta, np.transpose(theta))
    return ((1/(2 * X.shape[0])) * (np.sum((predict(X, theta) - y)**2)) + reg)

def get_regularization(theta, lbda, size, regularization):
    if regularization == "L1":
        reg = (lbda / (2 * size)) * np.sum(np.absolute(theta[1:]))
    elif regularization == "L2":
        reg = (lbda / (2 * size)) * np.sum(np.square(theta[1:]))
    return (reg)

def get_regularization_derived(theta, lbda, size, regularization):
    if regularization == "L1":
        reg = (lbda / (2 * size)) * (theta / np.absolute(theta))
    elif regularization == "L2":
        reg = (lbda / size) * theta
    reg[0] = 0
    return (reg)    
        
def mini_batch(X, y, batch_size):
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    for start_idx in range(0, X.shape[0] - batch_size + 1, batch_size):
        idx_batch = indices[start_idx:start_idx + batch_size]
        yield X[idx_batch], y[idx_batch]

def exponentionnal_decay(alpha_0, epochs, decay_rate):
    return(alpha_0 * np.exp(-decay_rate * epochs))

def gradient_descent(X, y, theta, 
                     alpha=0.01,
                     num_iters=1500,
                     batch_size=-1,
                     decay_rate=0.0,
                     tol=0.0001,
                     lbda=0.001,
                     regularization="L2"):
    m = X.shape[0]
    J_history = []
    alpha_0 = alpha
    b_size = m if (batch_size <= 0 or batch_size > m) else batch_size
    decay_rate = 0.0 if b_size == m else decay_rate
    prev_cost = 0
    
    for i in tqdm(range(num_iters)):
        
        # regularization
        reg = get_regularization_derived(theta, lbda, b_size, regularization)

        for batch in mini_batch(X, y, b_size):
            X_tmp, y_tmp = batch
            diff = np.dot((predict(X_tmp,theta) - y_tmp), X_tmp)
            theta = theta - alpha * (diff / m + reg)
            
            # tol
            curr_cost = cost(X_tmp, y_tmp, theta, lbda=lbda, regularization=regularization)
            if abs(prev_cost - curr_cost) < tol:
                print("training finished in {} iterations".format(i))
                return theta, J_history
            prev_cost = curr_cost
            J_history.append(curr_cost)        
        
        # learning rate decay
        alpha = exponentionnal_decay(alpha_0, i, decay_rate)
        

    return theta, J_history

def abline(slope, intercept):
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--')

def plot(df, theta, name):
    plt.clf()
    X = np.array(df[['km']]).flatten()
    y = np.array(df[['price']]).flatten()
    X, minn, maxx = featureNormalize(X)

    X = (X * (maxx - minn)) + minn
    theta[0] -= minn * (theta[1]) / (maxx - minn)
    theta[1] /= (maxx - minn)

    plt.scatter(X, y)
    abline(theta[1], theta[0])
    plt.savefig(name + ".png")
    plt.clf()


def get_arguments ():
    parser = argparse.ArgumentParser(description='Data generator program.')
    parser.add_argument('-f', '--file', default="Data/data.csv", help='file')
    res = parser.parse_args(sys.argv[1:])
    return (res.file)

def main():
    
    try:
        # Retrieving data
        filename = get_arguments()
        df = vaex.open(filename)
        X = np.array(df[['km']]).flatten()
        y = np.array(df[['price']]).flatten()

        # Feature normalize
        X, x_min, x_max = featureNormalize(X)

        # Add 1 vector for biais unit
        X = np.c_[np.ones(X.shape[0]), X]

        # Training the bonuses
        print("Training with weird parameters ...\n")
        theta = np.zeros(2)
        theta, J_history = gradient_descent(X, y, theta,
                        alpha=0.01,
                        num_iters=200,
                        decay_rate=0.0001, lbda=0.0001, batch_size=14)

        fit = plt.figure()
        ax = plt.axes()
        ax.plot(J_history)
        plt.savefig('cost_history_bonus.png')

        plot(df, theta, "visu_bonus")

        with open("Models/weights.csv", "w") as weight_file:
            weight_file.write("biais,weight\n")
            weight_file.write("{},{}\n".format(theta[0], theta[1]))

        # Training the model
        print("\nTraining on the data ...\n")
        theta = np.zeros(2)
        theta, J_history = gradient_descent(X, y, theta,
                        alpha=0.01,
                        num_iters=20000,
                        decay_rate=0.0, lbda=0.0)

        fit = plt.figure()
        ax = plt.axes()
        ax.plot(J_history)
        plt.savefig('cost_history.png')

        plot(df, theta, "visu")

        with open("Models/weights.csv", "w") as weight_file:
            weight_file.write("biais,weight\n")
            weight_file.write("{},{}\n".format(theta[0], theta[1]))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()