import random
import matplotlib
import matplotlib.pyplot as plt

N  = 5000 # Default size of population
mu = 100. # Default mean of population's wealth

def sample(distribution, N=N, mu=mu):
    "Sample from the distribution N times, then normalize results to have mean mu."
    return normalize([distribution() for _ in range(N)], mu * N)

def constant(mu=mu):          return mu
def uniform(mu=mu, width=mu): return random.uniform(mu-width/2, mu+width/2)
def gauss(mu=mu, sigma=mu/3): return random.gauss(mu, sigma) 
def beta(alpha=2, beta=3):    return random.betavariate(alpha, beta)
def pareto(alpha=4):          return random.paretovariate(alpha)
    
def normalize(numbers, total):
    "Scale the numbers so that they add up to total."
    factor = total / float(sum(numbers))
    return [x * factor for x in numbers]
	
	
def random_split(X, Y):
    "Take all the money in the pot and divide it randomly between X and Y."
    pot = X + Y
    m = random.uniform(0, pot)
    return m, pot - m
    
def winner_take_most(X, Y, most=3/4.): 
    "Give most of the money in the pot to one of the parties."
    pot = X + Y
    m = random.choice((most * pot, (1 - most) * pot))
    return m, pot - m

def winner_take_all(X, Y): 
    "Give all the money in the pot to one of the actors."
    return winner_take_most(X, Y, 1.0)

def redistribute(X, Y): 
    "Give 55% of the pot to the winner; 45% to the loser."
    return winner_take_most(X, Y, 0.55)

def redistribute_test(X, Y): 
    "Give 55% of the pot to the winner; 45% to the loser."
    return winner_take_most(X, Y, 0.64)
	
def perfect_redistribute(X, Y): 
    "Give exactly half of the pot to both parties"
    pot = X + Y
    m = pot / 2.
    return m, pot - m

def split_half_min(X, Y):
    """The poorer actor only wants to risk half his wealth; 
    the other actor matches this; then we randomly split the pot."""
    pot = min(X, Y)
    m = random.uniform(0, pot)
    return X - pot/2. + m, Y + pot/2. - m

	
	
def anyone(pop): return random.sample(range(len(pop)), 2)

def nearby(pop, k=5): 
    i = random.randrange(len(pop))
    j = i + random.choice((1, -1)) * random.randint(1, k)
    return i, (j % len(pop))
               
def nearby1(pop): return nearby(pop, 1)

def simulate(population, transaction_fn, interaction_fn, T, percentiles, record_every):
    "Run simulation for T steps; collect percentiles every 'record_every' time steps."
    results = []
    for t in range(T):
        i, j = interaction_fn(population)
        population[i], population[j] = transaction_fn(population[i], population[j]) 
        if t % record_every == 0:
            results.append(record_percentiles(population, percentiles))
    return results

def report(distribution=gauss, transaction_fn=random_split, interaction_fn=anyone, N=N, mu=mu, T=5*N, 
           percentiles=(1, 10, 25, 33.3, 50, -33.3, -25, -10, -1), record_every=25):
    "Print and plot the results of the simulation running T steps." 
    # Run simulation
    population = sample(distribution, N, mu)
    results = simulate(population, transaction_fn, interaction_fn, T, percentiles, record_every)
    # Print summary
    print('Simulation: {} * {}(mu={}) for T={} steps with {} doing {}:\n'.format(
          N, name(distribution), mu, T, name(interaction_fn), name(transaction_fn)))
    fmt = '{:6}' + '{:10.2f} ' * len(percentiles)
    print(('{:6}' + '{:>10} ' * len(percentiles)).format('', *map(percentile_name, percentiles)))
    #for (label, nums) in [('start', results[0]), ('mid', results[len(results)//2]), ('final', results[-1])]:
    #    print fmt.format(label, *nums)
    # Plot results
    for line in zip(*results):
        plt.plot(line)
    plt.show()

def record_percentiles(population, percentiles):
    "Pick out the percentiles from population."
    population = sorted(population, reverse=True)
    N = len(population)
    return [population[int(p*N/100.)] for p in percentiles]

def percentile_name(p):
    return ('median' if p == 50 else 
            '{} {}%'.format(('top' if p > 0 else 'bot'), abs(p)))
    
def name(obj):
    return getattr(obj, '__name__', str(obj))