import math
#import matplotlib.pyplot as pyplot
import random
import sys
import time

#Process the file and report the shortest path
def Main(argv):	
	if len(argv) == 6:
		numList = []
		for i in range(int(sys.argv[1])):
			numList.append(random.randint(1, 1000000))
		
		print('Genome')
		print(numList)
		
		startTime = time.time()
		
		experts = geneticAlgorithm(numList, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
		
		final = wisdomOfCrowds(numList, experts[:int(len(experts)*.25)])
		
		print('Time:\t' + str(time.time() - startTime))
		print('Final:\t' + str(final.fitness()) + '\nList1\n' + str(final.list1) + '\nList2\n' + str(final.list2))
		
	else:
		print('Missing Parameters\n [GenomeSize] [Number of Iterations] [Generations Per Iteration] [Number of Populations] [Population Size]')


def wisdomOfCrowds(baseGenome, experts):
	baseGenome.sort()
	weight1 = [0] * len(baseGenome)
	weight2 = [0] * len(baseGenome)
	
	for expert in experts:
		for i, gene in enumerate(baseGenome):
			if (expert.list1.count(gene) > 0):
				weight1[i] += 1
				expert.list1.remove(gene)
				
			if (expert.list2.count(gene) > 0):
				weight2[i] += 1
				expert.list2.remove(gene)
				
	for i, gene in enumerate(baseGenome):
		print('gene ' + str(gene) + '\tweight1 ' + str(weight1[i]) + '\tweight2 ' + str(weight2[i]))
	
	final = genome([], [])
	
	for i, gene in enumerate(baseGenome):
		if (weight1[i] > weight2[i]):
			final.list1.append(gene)
		elif (weight2[i] > weight1[i]):
			final.list2.append(gene)
		else:
			if (random.random() < .5):
				final.list1.append(gene)
			else:
				final.list2.append(gene)
	
	return final


#Performs the genetic algorithm based upon the starting conditions
def geneticAlgorithm(baseGenome, numIterations, numGenPerInter, numPops, initPopSize):
	populations = []
	
	for j in range(numPops):
		populations.append([])
		for i in range(initPopSize):
			random.shuffle(baseGenome)
			splitPoint = random.randint(1, len(baseGenome)-2)
			populations[j].append(genome(list(baseGenome[:splitPoint]), list(baseGenome[splitPoint:])))
			
	for i in range(numIterations):
		newPops = []
		for j, population in enumerate(populations):
			newPop = evolvePopulation(population, numGenPerInter)
			print(str(i) + ',' + str(j) + '\t' + str(newPop[0].fitness()))
			newPops.append(newPop)
		
		populations = mergePopulations(newPops, random.randint(1, numPops-1), random.randint(1, int(len(newPops[0])/numPops)))
	
	results = []
	for population in populations:
		results.extend(population)
	
	results.sort(key=lambda element: element.fitness())
	return results

def mergePopulations(populations, direction, numNomads):
	nomads = []
	for i in range(len(populations)):
		nomads.append([])
		for a in range(numNomads):
			nomads[i].append(populations[i].pop(random.randint(0, len(populations[i])-1)))
	
	for i, nomad in enumerate(nomads):
		j = i + direction
		if (j >= len(populations)):
			j -= len(populations)
		
		populations[j].extend(nomad)
	
	return populations
		
def evolvePopulation(population, numGenerations):
	leader = -1
	leaderCount = 0
	
	population.sort(key=lambda element: element.fitness())
	
	for count in range(numGenerations):
		
		population = nextGeneration(population)
		
		mutateChance = leaderCount * .01 + .05
		for i, genome in enumerate(population):
			if (random.random() < mutateChance):
				mutate(genome, 10)
				
		population.sort(key=lambda element: element.fitness())
		
		if (population[0] == leader):
			leaderCount += 1
		else:
			leader = population[0]
			leaderCount = 0
			
	return population

#Breeds the first third of a population with itself to generated the next generation
def nextGeneration(population):
	cutoff = int(len(population)/9)
	newpop = population[:cutoff*1]
	newpop.extend(population[cutoff*2:cutoff*3])
	newpop.extend(population[cutoff*4:cutoff*5])
	
	for i in range(cutoff*3):
		parent1 = newpop[i]
		parent2 = population[random.randint(0, len(population)-1)]
		
		newpop.append(crossover(parent1, parent2))
		newpop.append(crossover(parent2, parent1))
	
	return newpop

#Breeds two parents together and returns a child
def crossover(parent1, parent2):
	child = genome(list(parent1.list1), list(parent1.list2))
	
	if (len(parent2.list1) > 0):
		for i in range(random.randint(0, len(parent2.list1)-1)):
			value = random.choice(parent2.list1)
			if (child.list2.count(value) > 0):
				child.list2.remove(value)
				child.list1.append(value)
	
	if (len(parent2.list2) > 0):
		for i in range(random.randint(0, len(parent2.list2)-1)):
			value = random.choice(parent2.list2)
			if (child.list1.count(value) > 0):
				child.list1.remove(value)
				child.list2.append(value)
	
	return child

#mutates a genome
def mutate(genome, numSwaps):
	for i in range(numSwaps):
		if (random.random() < .5):
			if (len(genome.list1) > 0):
				genome.list2.append(genome.list1.pop(random.randint(0, len(genome.list1)-1)))
		else:
			if (len(genome.list2) > 0):
				genome.list1.append(genome.list2.pop(random.randint(0, len(genome.list2)-1)))

class genome:
	def __init__(self, list1, list2):
		self.list1 = list1
		self.list2 = list2
		
	def __str__(self):
		return('list1 ' + str(sum(self.list1)) + '\t' + 'list2 ' + str(sum(self.list2)))
	
	#calculates the fitness of a genome
	def fitness(self):
		return math.fabs(sum(self.list1)-sum(self.list2))

if __name__ == "__main__":
	Main(sys.argv)
