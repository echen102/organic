# NOTE: All lines should be limited to 80 characters (convention)
# Line breaks not added for easier viewing and teaching

# Structure of likelihood dictionary
# label (class) 
#   -> pixel (x,y position of pixel in img)
#       -> value (rgb value from 0-255)
#           -> number of occurances of this rgb value

from __future__ import division
import os
import pprint
import numpy as np
import pickle
import math

# global paths
path_train = 'mnist_train/'
path_test = 'mnist_test/'
path_likelihood = "likelihood.pkl"
path_prior = "priors.pkl"

# returns label and rest of data as a list of lists
def parse_file(path):
    f = open(path, 'r')
    data = []
    for line in f:
        data.append(line)
    f.close()
    return int(data[0]), data[1:]

# loads a pickle file and returns the object
def load_file(path): 
    f = open(path, 'r')
    loaded = pickle.load(f)
    f.close()
    return loaded

# saves a object to a pickle file
def save_pickle(path, data):
    f = open(path, 'wb')
    pickle.dump(data, f)
    f.close()

# Implements the training using files in found in 
# path_train directory. 
# Returns the generated likelihood and priors 
def train_img(): 

    # dictionary initiliazation 
    # count and probability kept separately for demonstration purposes
    # technically only needs to use one dict instead of two 

    # Calculates P(label)
    priors_count = {}
    priors_probability = {}

    # Calculate P(Fij = f| label)
    # (# of times pixel i,j has value f in the training values) / 
    # (total # of training examples from this label)
    likelihood_count = {}
    likelihood_probability = {}

    # laplace variables
    laplace_k = 0.00155
    laplace_d = laplace_k * (28 * 28 * 255)

    # iterate through all training files
    for path in os.listdir(path_train):

        label, data = parse_file(path_train + path)

        # update priors based on current label
        if label not in priors_count: 
            priors_count[label] = 1
        else: 
            priors_count[label] +=1

        if label not in likelihood_count:
            likelihood_count[label] = {}            

        # updates the count of (x,y) found with the corresponding pixel value 
        for x, line in enumerate(data):
            row = line.split()

            for y, value in enumerate(row):
                if (x,y) not in likelihood_count[label]:
                    likelihood_count[label][(x,y)] = {}
                    likelihood_count[label][(x,y)][value] = 1
                else: 
                    if value not in likelihood_count[label][(x,y)]: 
                        likelihood_count[label][(x,y)][value] = 1
                    else:
                        likelihood_count[label][(x,y)][value] +=1


    # converts prior and likelihood counts to probabilities 
    # (# of training files with current label) / (total # of training files)
    for label in priors_count: 
        priors_probability[label] =  priors_count[label] / len(os.listdir(path_train))

    # (# of times pixel i,j has pixel value in the training values) / (total # of training files from this label)
    for label in likelihood_count: 
        likelihood_probability[label] = {}
       
        for pixel in likelihood_count[label]: 
            likelihood_probability[label][pixel] = {}
            
            for value in likelihood_count[label][pixel]:
                likelihood_probability[label][pixel][value] = likelihood_count[label][pixel][value]
                
                if label in priors_count: 
                    likelihood_probability[label][pixel][value] = likelihood_count[label][pixel][value]/priors_count[label]

    # Applies laplace smoothening to offset 0 counts
    for label in likelihood_probability: 
        for pixel in likelihood_probability[label]:
            for value in xrange(256):
                if str(value) not in likelihood_probability[label][pixel]:
                    likelihood_probability[label][pixel][str(value)] = laplace_k/(priors_count[label]+laplace_d)
                else: 
                    likelihood_probability[label][pixel][str(value)] = (likelihood_count[label][pixel][str(value)] + laplace_k)/(priors_count[label]+laplace_d)

    # saves generated dictionaries to files
    # gives user option to load directly from file
    save_pickle(path_likelihood, likelihood_probability)
    save_pickle(path_prior, priors_probability)

    return priors_probability, likelihood_probability

# Iterates through test files and predicts number
def test_img(priors, likelihood):

    num_correct = 0
    num_total = len(os.listdir(path_test))

    # For current file, calculate the probability for each potential label
    # predicted number is the label that has the highest probability value
    for path in os.listdir(path_test):
        curr_probability = {}
        label, data = parse_file(path_test + path)

        for curr_label in priors: 
            curr_probability[curr_label] = 0

            for x, line in enumerate(data):
                row = line.split()

                for y, value in enumerate(row):
                    curr_probability[curr_label]+= np.log(likelihood[curr_label][(x,y)][value])

        predicted_num = max(curr_probability, key=curr_probability.get)
        
        # updates the number of correct predictions        
        if predicted_num == label: 
            num_correct +=1

    percent_accuracy = num_correct/num_total * 100
    print "Final Statistics"
    print "================"
    print ("Number Correct: %d" %(num_correct))
    print ("Out Of: %d" %(num_total))
    print ("Percent Accuracy: %0.2f%%" %(percent_accuracy))

def main():

    priors, likelihood_probability = train_img()

    stored_priors = load_file("priors.pkl")
    stored_likelihood = load_file("likelihood.pkl")

    test_img(stored_priors, stored_likelihood)

if __name__ == "__main__": 
    main()