# Maximize fitness function

import sys
import random
import math
import matplotlib.pyplot as plt
#from time import sleep
from tqdm import tqdm


rou = 5
pinfy = sys.maxsize
ninfy = -1 * sys.maxsize

def genInitPop(dim):
    
    particle = []
    
    for j in range(0, dim):
        x = random.randint(ninfy, pinfy)
        y = random.randint(ninfy, pinfy)
        alpha = round(x / math.sqrt(pow(x,2) + pow(y,2)), rou)
        beta = round(y / math.sqrt(pow(x,2) + pow(y,2)),rou)
        if random.uniform(-1, 1) > 0:
            beta = beta * (-1)
        particle.append([alpha, beta])
        
    return particle
        
def getInitialAngle(particle, dim):
    
    theta = []
    
    for i in range(dim):
        
        a = round(math.atan(particle[i][1] / particle[i][0]), rou)
        
        theta.append(a)
    
    return theta


def calFitness(v):
    
    return sum(v)
    
def observe(particle, dim):
    
    binary = []
    
    for i in range(dim):
        b = 0
        if random.uniform(0, 1) < pow(particle[i][0], 2):
            b = 0
        else:
            b = 1
        
        binary.append(b)
    return binary

def updateAngle(theta, thetaPb, thetaGb, dim):
    
    omega = 0.72
    phi = 1.65
    eta = 1.81
    r1 = random.uniform(0,1)
    r2 = random.uniform(0,1)
    delTheta = 0
    
    param1 = [omega * float(a) for a in theta]
    temp1 = [t1 - t2 for (t1, t2) in zip(thetaPb, theta)]
    param2 = [phi * r1 * diff for diff in temp1]
    temp2 = [t1 - t2 for (t1, t2) in zip(thetaGb, theta)]
    param3 = [eta * r2 * diff for diff in temp2]
        
    delTheta = [round(p1 + p2 + p3, rou) for (p1, p2, p3) in zip(param1, param2, param3)]
    
    return delTheta


def updateQubits(theta, particle, dim):
    
    #alpha = particle[0]
    #beta = particle[1]
    uQ = []
    for i in range(dim):
        uA = round(math.cos(theta[i]) * particle[i][0] - math.sin(theta[i]) * particle[i][1], rou) 
        uB = round(math.sin(theta[i]) * particle[i][0] + math.cos(theta[i]) * particle[i][1], rou)
        uQ.append([uA, uB])    
    
    return uQ

if __name__ == '__main__':
    
    pSize = 100
    pDimension = 100
    maxIte = 250
    population = []
    binary = []
    theta = []
    decodedValues = []
    
    print('-'*80)
    #Generating Initial Population
    print('Generating Initial Population:')
    for i in tqdm(range(pSize)):
        particle = genInitPop(pDimension)
        population.append(particle)
    
    print(population[0])
    
    print('-'*80)
    print('Observatoin')
    #Quantum observation
    for i in tqdm(range(pSize)):
        b = observe(population[i], pDimension)
        binary.append(b)
    print(binary[0])
    
    print('-'*80)
    print('Calculating Initial Angle')
    #Calculating Initial Angle
    for p in tqdm(range(pSize)):
        theta.append(getInitialAngle(population[p], pDimension))
    
    print('\n{}'.format(theta[0]))
    
    
    print('-'*80)
    
    #Initializing Local Best 
    #pB = []
    thetaPB = []
    fPB = []
    print('Calculating Local Best')
    for i in tqdm(range(pSize)):
        #pB.append(population[i])
        thetaPB.append(theta[i])
        fPB.append(calFitness(binary[i]))
    
    print('-'*80)
    
    #Initializing Global Best
    print('Calculating Global Best:')
    maxFitness = max(fPB)
    thetaGB = theta[fPB.index(maxFitness)]
    binGB = binary[fPB.index(maxFitness)]
    print('Index of Global Best Particle: {}, Fitness: {}\n{}'.format(fPB.index(maxFitness), maxFitness, binGB))
        
    print('-'*80)
    
    gBestFitness = []
    gBestFitness.append(maxFitness)
    
    #Main loop
    print('Runing Main Loop')
    for g in tqdm(range(maxIte)):
        
        for j in range(pSize):
            deltaTheta = updateAngle(theta[j], thetaPB[j], thetaGB, pDimension)
            #print('Updated Angle:')
            #print(deltaTheta)
            
            updatedQubits = updateQubits(deltaTheta, population[j], pDimension)
            #print('Updated Qubits:')
            #print(updatedQubits)
            
            updatedBinary = observe(updatedQubits, pDimension)
            updatedFitness = calFitness(updatedBinary)
            
            # Update local best
            if updatedFitness > fPB[j]:
                
                #pB[j] = updatedQubits
                thetaPB[j] = deltaTheta
                fPB[j] = updatedFitness
                
                #print('Local Best: {}'.format(pBest))
                # Update global best
                if updatedFitness > calFitness(binGB):

                    #gBest = pBest
                    thetaGB = deltaTheta
                    binGB = updatedBinary
                    #print('Global Best Fitness: {}'.format(calFitness(binGB)))
        
        gBestFitness.append(calFitness(binGB))
    
    #print('\n{}'.format(gBestFitness))
    print('\n')
    print('-'*80)
    
    finalFitness = gBestFitness[len(gBestFitness) - 1]
    print('Fitness: {}\n {}'.format(finalFitness, binGB))
    print('-'*80)
    
    #Plotting gBest Fitness Value
    plt.figure(figsize=(10, 5))
    plt.ylabel('Fitness Value')
    plt.xlabel('Generation')
    plt.plot(gBestFitness)
    plt.show()


    


        
    
    
    
    
        
    
        
        
        
        
        
        
