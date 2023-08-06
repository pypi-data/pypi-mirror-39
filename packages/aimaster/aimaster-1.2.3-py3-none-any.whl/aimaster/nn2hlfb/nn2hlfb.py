import numpy as np
from scipy.special import expit
from aimaster.tools import nnplotter
def createnn(architecture):
    if not isinstance(architecture,list):
        print("""give architecture as a list of neurons in each layer including
              input layer,hidden layers and output layer!
              Example: architecture=[2,3,3,1] for nn with input layer of 
                      2 neurons, two hidden layers with 3 neurons each(without 
                      counting bias) and an output layer of 1 neuron""")
