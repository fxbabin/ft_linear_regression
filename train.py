import vaex
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import random

def featureNormalize(X):
    mean = X.mean(axis=0)
    stdev = X.std(axis=0)
    X = (X - mean)/stdev
    return X, mean, stdev

def predict(X, theta):
    return(np.dot(X, theta))

def cost(X, y, theta):
    return ((1/(2 * X.shape[0])) * (np.sum((predict(X, theta) - y)**2)))

def fit_with_cost(X, y, theta, alpha, num_iters):
    m = X.shape[0]
    J_history = []
    for i in range(num_iters):
        theta = theta - (alpha/m) * np.dot((predict(X, theta) - y), X)
        J_history.append(cost(X, y, theta))
    return theta, J_history

# def get_batch_size(gradient_descent, batch_size, size):
#     batch_s = size
#     if gradient_descent == "batch":
#         decay_rate = 0.0
#     elif gradient_descent == "mini_batch":
#         batch_s = batch_size
#     elif gradient_descent == "stochastic":
#         batch_s = 1
#     return (batch_s)
    
# def get_regularization(theta, lbda, size, regularization):
#     if regularization == "L1":
#         reg = (lbda / size) * np.absolute(theta)
#     elif regularization == "L2":
#         reg = (lbda / size) * np.square(theta)
#     reg[0] = theta[0]
#     return (reg)

# def learning_rate_decay(alpha_0, epochs, decay_rate):
#     return((1 / (1 + decay_rate * epochs)) * alpha_0)

# def batch_generator(X, y, batch_size):
#     np.random.shuffle(X)
#     size = X.shape[0]
#     b_size = 0
#     batches_X = []
#     batches_y = []
#     while (b_size + batch_size) < size:
#         batches_X.append(X[b_size:(b_size + batch_size)])
#         batches_y.append(y[b_size:(b_size + batch_size)])
#         b_size += batch_size
#     batches_X.append(X[b_size:size])
#     batches_y.append(y[b_size:size])
#     nb_batches = size // batch_size
#     while True:
#         rand_nb = random.randint(0,nb_batches-1)
#         yield batches_X[rand_nb], batches_y[rand_nb]


# def complete_fit(X,
#                  y,
#                  theta, 
#                  alpha, 
#                  num_iters, 
#                  regularization="L1",
#                  lbda=0.01,
#                  gradient_descent="batch",
#                  batch_size=4,
#                  decay_rate=0.0):
    
#     m = X.shape[0]
#     J_history = []
#     alpha_0 = alpha
    
#     decay_rate = 0.0 if gradient_descent == "batch" else decay_rate
#     batch_size = get_batch_size(gradient_descent, batch_size, m)     
#     b_gen = batch_generator(X, y, batch_size)
    
#     for epoch in range(num_iters):
#         X_tmp, y_tmp = next(b_gen)
#         reg = get_regularization(theta, lbda, batch_size, regularization)
#         theta = theta - (alpha/m) * (np.dot((predict(X_tmp, theta) - y_tmp), X_tmp) + reg)
#         alpha = learning_rate_decay(alpha_0, epoch, decay_rate)
#         J_history.append(cost(X_tmp, y_tmp, theta))  
#     return theta, J_history


def main():
    
    # Retrieving data
    df = vaex.open("Data/data.csv")
    X = np.array(df[['km']]).flatten()
    y = np.array(df[['price']]).flatten()

    # Feature normalize
    X, mean, stdev = featureNormalize(X)

    # Add 1 vector for biais unit
    X = np.c_[np.ones(X.shape[0]), X]
    
    # Saving mean and stdev
    with open("Models/mean_stdev.csv", "w") as mean_file:
        mean_file.write("mean,stdev\n")
        mean_file.write("{},{}\n".format(mean, stdev))

    # Training the model
    theta = np.zeros(2)
    theta, J_history = fit_with_cost(X, y, theta, 0.01, 1500)

    with open("Models/weights.csv", "w") as mean_file:
        mean_file.write("biais,weight\n")
        mean_file.write("{},{}\n".format(theta[0], theta[1]))
    print(theta)

if __name__ == "__main__":
    main()