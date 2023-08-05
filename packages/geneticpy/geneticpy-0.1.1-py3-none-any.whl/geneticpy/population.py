import random
from copy import deepcopy
from geneticpy.distributions.distribution_base import DistributionBase
from geneticpy.parameter_set import ParameterSet

class Population:
    def __init__(self, fn, params, size, percentage_to_randomly_spawn=0.05, mutate_chance=0.25, retain_percentage=0.6,
                 maximize_fn=False, tqdm_obj=None):
        assert isinstance(params, dict)

        self.fn = fn
        self.params = params
        self.size = size
        self.maximize_fn = maximize_fn
        self.percentage_to_randomly_spawn = percentage_to_randomly_spawn
        self.mutate_chance = mutate_chance
        self.retain_percentage = retain_percentage
        self.tqdm_obj = tqdm_obj
        self.grades = None
        self.population = [self.create_random_set() for _ in range(self.size)]

    def evolve(self):
        indiv_iter = 0
        graded = []
        for indiv in self.population:
            indiv_iter += 1
            graded.append((indiv.get_score(), indiv))
        self.grades = sorted(graded, key=lambda x: x[0], reverse=self.maximize_fn)
        graded = [x[1] for x in self.grades]
        retained_length = int(len(graded) * self.retain_percentage)
        keep = graded[:retained_length]
        m_count = 0
        s_count = 0
        b_count = 0
        for indiv in keep:
            if self.mutate_chance > random.random():
                new_indiv = deepcopy(indiv)
                m_count += 1
                keep.append(new_indiv.mutate())

        for i in range(int(self.size * self.percentage_to_randomly_spawn)):
            keep.append(self.create_random_set())
            s_count += 1

        while len(keep) < self.size:
            set1 = random.randint(0, retained_length - 1)
            set2 = random.randint(0, retained_length - 1)
            if set1 != set2:
                b_count += 1
                keep.append(keep[set1].breed(keep[set2]))
        self.population = keep

    def get_final_scores(self):
        net_iter = 0
        graded = []
        for indiv in self.population:
            net_iter += 1
            if self.tqdm_obj is not None:
                self.tqdm_obj.update()
            graded.append((indiv.get_score(), indiv))
        self.grades = sorted(graded, key=lambda x: x[0], reverse=self.maximize_fn)
        graded = [x[1] for x in self.grades]
        self.population = graded

    def get_top_score(self):
        return self.population[0].get_score()

    def get_top_params(self):
        return self.population[0].params

    def create_random_set(self):
        random_params = {k: v.pull_value() if isinstance(v, DistributionBase) else v for k, v in self.params.items()}
        return ParameterSet(params=random_params, param_space=self.params, fn=self.fn, maximize_fn=self.maximize_fn,
                            tqdm_obj=self.tqdm_obj)
