""" Classes for defining state optimization problems.

    Author: Genevieve Hayes
    License: 3-clause BSD license.
"""
import numpy as np
from sklearn.metrics import mutual_info_score
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree, depth_first_tree
from .fitness import TravellingSales

class OptProb:
    """Base class for state optimisation problems."""

    def __init__(self, length, fitness_fn, maximize=True):
        """Initialize OptProb object.

        Args:
        length: int. Number of elements in state vector
        fitness_fn: fitness function object. Object to implement
        fitness function
        for optimization.
        max_val: int. Number of unique values that each element could take.
        maximize: bool. Whether to maximize the fitness function.
        Set False for minimization problem.

        Returns:
        None
        """
        if length < 0:
            raise Exception("""length must be a positive integer.""")
        elif not isinstance(length, int):
            if length.is_integer():
                self.length = int(length)
            else:
                raise Exception("""length must be a positive integer.""")
        else:
            self.length = length

        self.state = np.array([0]*self.length)
        self.neighbors = []
        self.fitness_fn = fitness_fn
        self.fitness = 0
        self.population = []
        self.pop_fitness = []
        self.mate_probs = []

        if maximize:
            self.maximize = 1.0
        else:
            self.maximize = -1.0

    def best_child(self):
        """Return the best state in the current population.

        Args:
        None

        Returns:
        best: array. State vector defining best child.
        """
        best = self.population[np.argmax(self.pop_fitness)]

        return best

    def best_neighbor(self):
        """Return the best neighbor of current state

        Args:
        None

        Returns:
        best: array. State vector defining best neighbor.
        """
        fitness_list = []

        for neigh in self.neighbors:
            fitness = self.eval_fitness(neigh)
            fitness_list.append(fitness)

        best = self.neighbors[np.argmax(fitness_list)]

        return best

    def eval_fitness(self, state):
        """Evaluate the fitness of a state vector

        Args:
        state: array. State vector for evaluation.

        Returns:
        fitness: float. Value of fitness function.
        """
        if len(state) != self.length:
            raise Exception("state length must match problem length")

        fitness = self.maximize*self.fitness_fn.evaluate(state)

        return fitness

    def eval_mate_probs(self):
        """
        Calculate the probability of each member of the population reproducing.

        Args:
        None

        Returns:
        None
        """
        pop_fitness = np.copy(self.pop_fitness)
        
        # Set -1*inf values to 0 to avoid dividing by sum of infinity.
        # This forces mate_probs for these pop members to 0.
        pop_fitness[pop_fitness == -1.0*np.inf] = 0
        
        if np.sum(pop_fitness) == 0:
            self.mate_probs = np.ones(len(pop_fitness)) \
                              / len(pop_fitness)
        else:
            self.mate_probs = pop_fitness/np.sum(pop_fitness)

    def get_fitness(self):
        """ Return the fitness of the current state vector.

        Args:
        None

        Returns:
        self.fitness: float. Fitness value of current state vector.
        """
        return self.fitness

    def get_length(self):
        """ Return the state vector length.

        Args:
        None

        Returns:
        self.length: int. Length of state vector.
        """
        return self.length

    def get_mate_probs(self):
        """ Return the population mate probabilities

        Args:
        None

        Returns:
        self.mate_probs: array. Numpy array containing mate probabilities of
        the current population
        """
        return self.mate_probs

    def get_maximize(self):
        """ Return the maximization multiplier

        Args:
        None

        Returns:
        self.maximize: int. Maximization multiplier
        """
        return self.maximize

    def get_pop_fitness(self):
        """ Return the current population fitness array

        Args:
        None

        Returns:
        self.pop_fitness: array. Numpy array containing the fitness values
        for the current population.
        """
        return self.pop_fitness

    def get_population(self):
        """ Return the current population

        Args:
        None

        Returns:
        self.population: array. Numpy array containing current population.
        """
        return self.population

    def get_state(self):
        """ Return the current state vector

        Args:
        None

        Returns:
        self.state: array. Current state vector.
        """
        return self.state

    def set_population(self, new_population):
        """ Change the current population to a specified new population and get
        the fitness of all members

        Args:
        new_population: array. Numpy array containing new population.

        Returns:
        None
        """
        self.population = new_population

        # Calculate fitness
        pop_fitness = []

        for i in range(len(self.population)):
            fitness = self.eval_fitness(self.population[i])
            pop_fitness.append(fitness)

        self.pop_fitness = np.array(pop_fitness)

    def set_state(self, new_state):
        """
        Change the current state vector to a specified value
        and get its fitness

        Args:
        new_state: array. New state vector value.

        Returns:
        None
        """
        if len(new_state) != self.length:
            raise Exception("""new_state length must match problem length""")

        self.state = new_state
        self.fitness = self.eval_fitness(self.state)


class DiscreteOpt(OptProb):
    """Child class for discrete state optimisation problems."""

    def __init__(self, length, fitness_fn, maximize=True, max_val=2):
        """Initialize OptProb object.

        Args:
        length: int. Number of elements in state vector
        fitness_fn: fitness function object. Object to implement
        fitness function for optimization.
        maximize: bool. Whether to maximize the fitness function.
        Set False for minimization problem.
        max_val: int. Number of unique values that each element could take.

        Returns:
        None
        """
        OptProb.__init__(self, length, fitness_fn, maximize)

        if self.fitness_fn.get_prob_type() == 'continuous':
            raise Exception("""fitness_fn must have problem type 'discrete',"""
                            + """ 'either' or 'tsp'. Define problem as"""
                            + """ ContinuousOpt problem or use alternative"""
                            + """ fitness function."""
                            )

        if max_val < 0:
            raise Exception("""max_val must be a positive integer.""")
        elif not isinstance(max_val, int):
            if max_val.is_integer():
                self.max_val = int(max_val)
            else:
                raise Exception("""max_val must be a positive integer.""")
        else:
            self.max_val = max_val

        self.keep_sample = []
        self.node_probs = np.zeros([self.length, self.max_val, self.max_val])
        self.parent_nodes = []
        self.sample_order = []
        self.prob_type = 'discrete'

    def eval_node_probs(self):
        """Update probability density estimates.

        Args:
        None

        Returns:
        None
        """
        # Create mutual info matrix
        mutual_info = np.zeros([self.length, self.length])
        for i in range(self.length - 1):
            for j in range(i + 1, self.length):
                mutual_info[i, j] = -1 * mutual_info_score(
                    self.keep_sample[:, i],
                    self.keep_sample[:, j])

        # Find minimum spanning tree of mutual info matrix
        mst = minimum_spanning_tree(csr_matrix(mutual_info))

        # Convert minimum spanning tree to depth first tree with node 0 as root
        dft = depth_first_tree(csr_matrix(mst.toarray()), 0, directed=False)
        dft = dft.toarray()

        # Determine parent of each node
        parent = np.argmin(dft[:, 1:], axis=0)

        # Get probs
        probs = np.zeros([self.length, self.max_val, self.max_val])

        probs[0, :] = np.histogram(self.keep_sample[:, 0],
                                   np.arange(self.max_val + 1),
                                   density=True)[0]

        for i in range(1, self.length):
            for j in range(self.max_val):
                subset = self.keep_sample[np.where(
                    self.keep_sample[:, parent[i - 1]] == j)[0]]

                if not len(subset):
                    probs[i, j] = 1/self.max_val
                else:
                    probs[i, j] = np.histogram(subset[:, i],
                                               np.arange(self.max_val + 1),
                                               density=True)[0]

        # Update probs and parent
        self.node_probs = probs
        self.parent_nodes = parent

    def find_neighbors(self):
        """Find all neighbors of the current state

        Args:
        None

        Returns:
        None
        """
        self.neighbors = []

        if self.max_val == 2:
            for i in range(self.length):
                neighbor = np.copy(self.state)
                neighbor[i] = np.abs(neighbor[i] - 1)
                self.neighbors.append(neighbor)

        else:
            for i in range(self.length):
                vals = list(np.arange(self.max_val))
                vals.remove(self.state[i])

                for j in vals:
                    neighbor = np.copy(self.state)
                    neighbor[i] = j
                    self.neighbors.append(neighbor)

    def find_sample_order(self):
        """Determine order in which to generate sample vector elements

        Args:
        None

        Returns:
        None
        """
        sample_order = []
        last = [0]
        parent = np.array(self.parent_nodes)

        while len(sample_order) < self.length:
            inds = []

            for i in last:
                inds += list(np.where(parent == i)[0] + 1)

            sample_order += last
            last = inds

        self.sample_order = sample_order

    def find_top_pct(self, keep_pct):
        """Select samples with fitness in the top n percentile.

        Args:
        keep_pct: float. Proportion of samples to keep.

        Returns:
        None
        """
        if (keep_pct < 0) or (keep_pct > 1):
            raise Exception("""keep_pct must be between 0 and 1.""")

        # Determine threshold
        theta = np.percentile(self.pop_fitness, 100*(1 - keep_pct))

        # Determine samples for keeping
        keep_inds = np.where(self.pop_fitness >= theta)[0]

        # Determine sample for keeping
        self.keep_sample = self.population[keep_inds]
    
    def get_keep_sample(self):
        """ Return the keep sample.

        Args:
        None

        Returns:
        self.keep_sample: array. Numpy array containing samples with fitness
        in the top n percentile.
        """
        return self.keep_sample

    def get_prob_type(self):
        """ Return the problem type.

        Args:
        None

        Returns:
        self.prob_type: string. Returns problem type.
        """
        return self.prob_type
    
    def random(self):
        """Return a random state vector

        Args:
        None

        Returns:
        state: array. Randomly generated state vector.
        """
        state = np.random.randint(0, self.max_val, self.length)

        return state

    def random_neighbor(self):
        """Return random neighbor of current state vector

        Args:
        None

        Returns:
        neighbor: array. State vector of random neighbor.
        """
        neighbor = np.copy(self.state)
        i = np.random.randint(0, self.length)

        if self.max_val == 2:
            neighbor[i] = np.abs(neighbor[i] - 1)

        else:
            vals = list(np.arange(self.max_val))
            vals.remove(neighbor[i])
            neighbor[i] = vals[np.random.randint(0, self.max_val-1)]

        return neighbor

    def random_pop(self, pop_size):
        """Create a population of random state vectors

        Args:
        pop_size: int. Size of population to be created.

        Returns:
        None
        """
        if pop_size <= 0:
            raise Exception("""pop_size must be a positive integer.""")
        elif not isinstance(pop_size, int):
            if pop_size.is_integer():
                pop_size = int(pop_size)
            else:
                raise Exception("""pop_size must be a positive integer.""")

        population = []
        pop_fitness = []

        for _ in range(pop_size):
            state = self.random()
            fitness = self.eval_fitness(state)

            population.append(state)
            pop_fitness.append(fitness)

        self.population = np.array(population)
        self.pop_fitness = np.array(pop_fitness)

    def reproduce(self, parent_1, parent_2, mutation_prob=0.1):
        """Create child state vector from two parent state vectors.

        Args:
        parent_1: array. State vector for parent 1.
        parent_2: array. State vector for parent 2.
        mutation_prob: float. Probability of a mutation at each
        state element during reproduction.

        Returns:
        child: array. Child state vector produced from parents 1 and 2.
        """
        if len(parent_1) != self.length or len(parent_2) != self.length:
            raise Exception("""Lengths of parents must match problem length""")

        if (mutation_prob < 0) or (mutation_prob > 1):
            raise Exception("""mutation_prob must be between 0 and 1.""")

        # Reproduce parents
        _n = np.random.randint(self.length - 1)
        child = np.array([0]*self.length)
        child[0:_n+1] = parent_1[0:_n+1]
        child[_n+1:] = parent_2[_n+1:]

        # Mutate child
        rand = np.random.uniform(size=self.length)
        mutate = np.where(rand < mutation_prob)[0]

        if self.max_val == 2:
            for i in mutate:
                child[i] = np.abs(child[i] - 1)

        else:
            for i in mutate:
                vals = list(np.arange(self.max_val))
                vals.remove(child[i])
                child[i] = vals[np.random.randint(0, self.max_val-1)]

        return child

    def reset(self):
        """Set the current state vector to a random value and get its fitness

        Args:
        None

        Returns:
        None
        """
        self.state = self.random()
        self.fitness = self.eval_fitness(self.state)

    def sample_pop(self, sample_size):
        """Generate new sample from probability density

        Args:
        sample_size: int. Size of sample to be generated.

        Returns:
        new_sample: array. Numpy array containing new sample.
        """
        if sample_size <= 0:
            raise Exception("""sample_size must be a positive integer.""")
        elif not isinstance(sample_size, int):
            if sample_size.is_integer():
                sample_size = int(sample_size)
            else:
                raise Exception("""sample_size must be a positive integer.""")

        # Initialize new sample matrix
        new_sample = np.zeros([sample_size, self.length])

        # Get value of first element in new samples
        new_sample[:, 0] = np.random.choice(self.max_val, sample_size,
                                            p=self.node_probs[0, 0])

        # Get sample order
        self.find_sample_order()
        sample_order = self.sample_order[1:]

        # Get values for remaining elements in new samples
        for i in sample_order:
            par_ind = self.parent_nodes[i-1]

            for j in range(self.max_val):
                inds = np.where(new_sample[:, par_ind] == j)[0]
                new_sample[inds, i] = np.random.choice(self.max_val,
                                                       len(inds),
                                                       p=self.node_probs[i, j])

        return new_sample


class ContinuousOpt(OptProb):
    """Child class for continuous state optimisation problems."""

    def __init__(self, length, fitness_fn, maximize=True, min_val=0,
                 max_val=1, step=0.1):
        """Initialize OptProb object.

        Args:
        length: int. Number of elements in state vector
        fitness_fn: fitness function object. Object to implement
        fitness function for optimization.
        maximize: bool. Whether to maximize the fitness function.
        Set False for minimization problem.
        min_val: float. Minimum value that each element could take.
        max_val: float. Maximum value that each element could take.
        step: float. Step size used in determining neighbors.

        Returns:
        None
        """
        OptProb.__init__(self, length, fitness_fn, maximize=maximize)

        if (self.fitness_fn.get_prob_type() != 'continuous') \
           and (self.fitness_fn.get_prob_type() != 'either'):
            raise Exception("fitness_fn must have problem type 'continuous'"
                            + """ or 'either'. Define problem as"""
                            + """ DiscreteOpt problem or use alternative"""
                            + """ fitness function."""
                            )

        if max_val <= min_val:
            raise Exception("""max_val must be greater than min_val.""")

        if step <= 0:
            raise Exception("""step size must be positive.""")

        if (max_val - min_val) < step:
            raise Exception("""step size must be less than"""
                            + """ (max_val - min_val).""")

        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.prob_type = 'continuous'

    def calculate_updates(self):
        """Calculate gradient descent updates.

        Args:
        None

        Returns:
        updates: list. List of back propagation weight updates.
        """
        updates = self.fitness_fn.calculate_updates()

        return updates

    def find_neighbors(self):
        """Find all neighbors of the current state.

        Args:
        None

        Returns:
        None
        """
        self.neighbors = []

        for i in range(self.length):
            for j in [-1, 1]:
                neighbor = np.copy(self.state)
                neighbor[i] += j*self.step

                if neighbor[i] > self.max_val:
                    neighbor[i] = self.max_val

                elif neighbor[i] < self.min_val:
                    neighbor[i] = self.min_val

                if not np.array_equal(np.array(neighbor), self.state):
                    self.neighbors.append(neighbor)

    def get_prob_type(self):
        """ Return the problem type.

        Args:
        None

        Returns:
        self.prob_type: string. Returns problem type.
        """
        return self.prob_type

    def random(self):
        """Return a random state vector

        Args:
        None

        Returns:
        state: array. Randomly generated state vector.
        """
        state = np.random.uniform(self.min_val, self.max_val, self.length)

        return state

    def random_neighbor(self):
        """Return random neighbor of current state vector

        Args:
        None

        Returns:
        neighbor: array. State vector of random neighbor.
        """
        while True:
            neighbor = np.copy(self.state)
            i = np.random.randint(0, self.length)

            neighbor[i] += self.step*np.random.choice([-1, 1])

            if neighbor[i] > self.max_val:
                neighbor[i] = self.max_val

            elif neighbor[i] < self.min_val:
                neighbor[i] = self.min_val

            if not np.array_equal(np.array(neighbor), self.state):
                break

        return neighbor

    def random_pop(self, pop_size):
        """Create a population of random state vectors

        Args:
        pop_size: int. Size of population to be created.

        Returns:
        None
        """
        if pop_size <= 0:
            raise Exception("""pop_size must be a positive integer.""")
        elif not isinstance(pop_size, int):
            if pop_size.is_integer():
                pop_size = int(pop_size)
            else:
                raise Exception("""pop_size must be a positive integer.""")

        population = []
        pop_fitness = []

        for _ in range(pop_size):
            state = self.random()
            fitness = self.eval_fitness(state)

            population.append(state)
            pop_fitness.append(fitness)

        self.population = np.array(population)
        self.pop_fitness = np.array(pop_fitness)

    def reproduce(self, parent_1, parent_2, mutation_prob=0.1):
        """Create child state vector from two parent state vectors.

        Args:
        parent_1: array. State vector for parent 1.
        parent_2: array. State vector for parent 2.
        mutation_prob: float. Probability of a mutation at each
        state element during reproduction.

        Returns:
        child: array. Child state vector produced from parents 1 and 2.
        """
        if len(parent_1) != self.length or len(parent_2) != self.length:
            raise Exception("""Lengths of parents must match problem length""")

        if (mutation_prob < 0) or (mutation_prob > 1):
            raise Exception("""mutation_prob must be between 0 and 1.""")

        # Reproduce parents
        _n = np.random.randint(self.length - 1)
        child = np.array([0.0]*self.length)
        child[0:_n+1] = parent_1[0:_n+1]
        child[_n+1:] = parent_2[_n+1:]
        # Mutate child
        rand = np.random.uniform(size=self.length)
        mutate = np.where(rand < mutation_prob)[0]

        for i in mutate:
            child[i] = np.random.uniform(self.min_val, self.max_val)

        return child

    def reset(self):
        """Set the current state vector to a random value and get its fitness

        Args:
        None

        Returns:
        None
        """
        self.state = self.random()
        self.fitness = self.eval_fitness(self.state)

    def update_state(self, updates):
        """Update current state given a vector of updates

        Args:
        updates: array. Update array.

        Returns:
        updated_state: array. Current state adjusted for updates
        """
        if len(updates) != self.length:
            raise Exception("""Length of updates must match problem length""")

        updated_state = self.state + updates

        updated_state[updated_state > self.max_val] = self.max_val
        updated_state[updated_state < self.min_val] = self.min_val

        return updated_state


class TSPOpt(DiscreteOpt):
    """Child class for travelling salesperson optimisation problems."""

    def __init__(self, length, fitness_fn=None, maximize=False, coords=None, 
                 distances=None):
        """Initialize OptProb object.

        Args:
        length: int. Number of elements in state vector. Must equal number of
        cities in the tour.
        fitness_fn: fitness function object. Object to implement
        fitness function for optimization.
        maximize: bool. Whether to maximize the fitness function.
        Set False for minimization problem.
        coords: list of pairs. Ordered list of the (x, y) co-ordinates of all
        nodes. This assumes that travel between all pairs of nodes is 
        possible. If this is not the case, then use distances instead. This 
        argument is ignored if fitness_fn is not None.
        distances: list of triples. List giving the distances, d, between all 
        pairs of nodes, u and v, for which travel is possible, with each 
        list item in the form (u, v, d). Order of the nodes does not matter, 
        so (u, v, d) and (v, u, d) are considered to be the same. If a pair is
        missing from the list, it is assumed that travel between the two 
        nodes is not possible. This argument is ignored if fitness_fn or 
        coords is not None.

        Returns:
        None
        """
        
        if (fitness_fn is None) and (coords is None) and (distances is None):
            raise Exception("""At least one of fitness_fn, coords and"""
                            + """ distances must be specified.""")
        elif fitness_fn is None:
            fitness_fn = TravellingSales(coords=coords, distances=distances)
        
        DiscreteOpt.__init__(self, length, fitness_fn, maximize, 
                             max_val = length)

        if self.fitness_fn.get_prob_type() != 'tsp':
            raise Exception("""fitness_fn must have problem type 'tsp'.""")

        self.prob_type = 'tsp'

    def adjust_probs(self, probs):
        """Normalize a vector of probabilities so that the vector sums to 1.
        
        Args:
        probs: array. Vector of probabilities that may or may not sum to 1. 
        
        Returns:
        adj_probs: array. Vector of probabilities that sums to 1. Returns a 
        zero vector if sum(probs) = 0.
        """
        if np.sum(probs) == 0:
            adj_probs = np.zeros(np.shape(probs))
        
        else:
            adj_probs = probs/np.sum(probs)
        
        return adj_probs
                    
    def find_neighbors(self):
        """Find all neighbors of the current state

        Args:
        None

        Returns:
        None
        """
        self.neighbors = []
        
        for node1 in range(self.length - 1):
            for node2 in range(node1 + 1, self.length):
                neighbor = np.copy(self.state)
                
                neighbor[node1] = self.state[node2]
                neighbor[node2] = self.state[node1]
                self.neighbors.append(neighbor)

    def random(self):
        """Return a random state vector

        Args:
        None

        Returns:
        state: array. Randomly generated state vector.
        """
        '''
        state = np.hstack(([self.start_node], 
                           np.random.permutation(self.node_vals)))
        '''
        state = np.random.permutation(self.length)
        
        return state

    def random_mimic(self):
        """Generate single MIMIC sample from probability density
        
        Args:
        None
        
        Returns:
        state: array. State vector of MIMIC random sample.
        """
        remaining = list(np.arange(self.length))
        state = np.zeros(self.length, dtype = np.int8)
        sample_order = self.sample_order[1:]
        node_probs = np.copy(self.node_probs)
        
        # Get value of first element in new sample
        state[0] = np.random.choice(self.length, p=node_probs[0, 0])
        remaining.remove(state[0])
        node_probs[:, :, state[0]] = 0

        # Get sample order
        self.find_sample_order()
        sample_order = self.sample_order[1:]
        
        # Set values of remaining elements of state
        for i in sample_order:
            par_ind = self.parent_nodes[i-1]
            par_value = state[par_ind]
            probs = node_probs[i, par_value]
            
            if np.sum(probs) == 0:
                next_node = np.random.choice(remaining)
                
            else:
                adj_probs = self.adjust_probs(probs)
                next_node = np.random.choice(self.length, p = adj_probs)
                
            state[i] = next_node
            remaining.remove(next_node)
            node_probs[:, :, next_node] = 0
        
        return state        
    
    def random_neighbor(self):
        """Return random neighbor of current state vector

        Args:
        None

        Returns:
        neighbor: array. State vector of random neighbor.
        """
        neighbor = np.copy(self.state)
        node1, node2 = np.random.choice(np.arange(self.length), 
                                        size = 2, replace = False)
        
        neighbor[node1] = self.state[node2]
        neighbor[node2] = self.state[node1]
        
        return neighbor

    def reproduce(self, parent_1, parent_2, mutation_prob=0.1):
        """Create child state vector from two parent state vectors.

        Args:
        parent_1: array. State vector for parent 1.
        parent_2: array. State vector for parent 2.
        mutation_prob: float. Probability of a mutation at each
        state element during reproduction.

        Returns:
        child: array. Child state vector produced from parents 1 and 2.
        """
        if len(parent_1) != self.length or len(parent_2) != self.length:
            raise Exception("""Lengths of parents must match problem length""")

        if (mutation_prob < 0) or (mutation_prob > 1):
            raise Exception("""mutation_prob must be between 0 and 1.""")

        # Reproduce parents
        _n = np.random.randint(self.length - 1)
        child = np.array([0]*self.length)
        child[0:_n+1] = parent_1[0:_n+1]
        
        unvisited = [node for node in parent_2 if node not in parent_1[0:_n+1]]
        child[_n+1:] = unvisited

        # Mutate child
        rand = np.random.uniform(size=self.length)
        mutate = np.where(rand < mutation_prob)[0]
        
        if len(mutate) > 0:
            mutate_perm = np.random.permutation(mutate)
            temp = np.copy(child)
            
            for i in range(len(mutate)):
                child[mutate[i]] = temp[mutate_perm[i]]
        
        return child
        
    def sample_pop(self, sample_size):
        """Generate new sample from probability density

        Args:
        sample_size: int. Size of sample to be generated.

        Returns:
        new_sample: array. Numpy array containing new sample.
        """
        if sample_size <= 0:
            raise Exception("""sample_size must be a positive integer.""")
        elif not isinstance(sample_size, int):
            if sample_size.is_integer():
                sample_size = int(sample_size)
            else:
                raise Exception("""sample_size must be a positive integer.""")
        
        self.find_sample_order()
        new_sample = []
        
        for _ in range(sample_size):
            state = self.random_mimic()
            new_sample.append(state)
        
        new_sample = np.array(new_sample)
        
        return new_sample
