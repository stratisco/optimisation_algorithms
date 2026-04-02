import random
from context import STAFF_DICT, PROJECTS_DICT


OPTIMISATIONS = True

MUTATE_ROW_FLIP = False


__cost_cache:dict = {}
def vectorCost(vector: list[list[int]]) -> float:
    '''
    cache flag forces cost caching to either be off or on. otherwise it defaults to OPTIMISATION
    '''

    # cache key is a tuple bc apparently they are faster than using strings (google said so it must be true)
    cache_key = tuple(tuple(a) for a in vector)

    if OPTIMISATIONS and cache_key in __cost_cache:
        return __cost_cache[cache_key]


    _a = 0.20
    _b = 0.20
    _d = 0.20
    _t = 0.20
    _y = 0.20

    overwork_penalty = 0
    skill_penalty = 0
    difficulty_penalty = 0
    deadline_penalty = 0

    # unique assignment
    assignment_violation = sum(abs(sum(a) - 1) for a in vector)

    staff_projects = {staff_id: [] for staff_id in STAFF_DICT}
    for project_i, assignments in enumerate(vector):
        project = PROJECTS_DICT[project_i + 1]
        for staff_i, assigned in enumerate(assignments):
            if assigned:
                staff_projects[staff_i + 1] += [project]

    for staff_id, projects in staff_projects.items():
        if not projects:
            continue  # if staff member has no assignments then skip

        staff = STAFF_DICT[staff_id]

        # capacity constraint
        total_time = sum(p.estimated_time for p in projects)
        overwork_penalty += max(0, total_time - staff.available_hours)

        for project in projects:
            # skill level constraint
            difficulty_penalty += max(0, project.difficulty - staff.skill_level)

            # skill matching
            if project.required_skill not in staff.skills:
                skill_penalty += 1

        # deadline penalty
        time_sum = 0
        for project in sorted(projects, key=lambda p: p.estimated_time):
            time_sum += project.estimated_time
            deadline_penalty += max(0, time_sum - project.deadline)

    out = _a * overwork_penalty + _b * skill_penalty + _d * difficulty_penalty + _t * deadline_penalty + _y * assignment_violation

    if OPTIMISATIONS:
        __cost_cache[cache_key] = out

    return out


class Chromosome:
    
    @staticmethod
    def crossoverChild(parent1:"Chromosome", parent2:"Chromosome") -> "Chromosome":
        split = random.randrange(len(parent1.getVector())+1)

        return Chromosome(parent1.getVector(True)[:split] + parent2.getVector(True)[split:])


    def __init__(self, vector=None):
        self.__vector = []
        
        for _ in range(len(PROJECTS_DICT)):
            if OPTIMISATIONS:
                row = [0] * len(STAFF_DICT)
                row[random.randint(0, len(STAFF_DICT) - 1)] = 1

            else:
                row = [random.randint(0, 1) for _ in range(len(STAFF_DICT))]
        
            self.__vector += [row]

        if vector != None:
            self.__vector = vector


    def getCost(self) -> float:
        return vectorCost(self.getVector())


    def mutate(self):
        # flip a random staff assignment for a random project row
        vec = self.getVector()


        if MUTATE_ROW_FLIP:
            # flip a random row
            row = random.randrange(len(vec))
            vec[row] = vec[row][::-1]


        # flip a random bit
        for _ in range(2):
            i = random.randrange(len(vec))
            j = random.randrange(len(vec[0]))
            vec[i][j] ^= 1


    def getVector(self, clone=False):
        if not clone:
            return self.__vector
        
        return [row[:] for row in self.getVector()]


    def clone(self) -> "Chromosome":
        return Chromosome(self.getVector(True))


    def printVector(self):
        print("[\n" + "\n".join(f"  {row}," for row in self.getVector()) + "\n]")
    

    def __str__(self, cost:bool=True) -> str:
        out = ''
        for projectId, assignments in enumerate(self.getVector()):
            staffList = []

            for staffId, assigned in enumerate(assignments):
                if assigned:
                    staffList += [staffId + 1]

            out += f'P{projectId + 1} -> ' + ', '.join([f'S{staffId}' for staffId in staffList]) + '\n'

        if cost:
            out += f'  Cost: {self.getCost()}' + '\n'

        return out


def tournament_selection(population:list[Chromosome], subsize:int=5) -> list[Chromosome]:
    return sorted(random.sample(population, subsize), key=lambda x: x.getCost())[:2]


if __name__ == '__main__':

    OPTIMISATIONS = False

    c = Chromosome([[1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]])
    assert c.getCost() == 6.4
    print(c.getCost())
    
    c = Chromosome([[0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0]])
    assert c.getCost() == 5.2
    print(c.getCost())

    c = Chromosome([[1, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 1], [0, 0, 1, 0, 0], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 1, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0]])
    assert c.getCost() == 2.8    
    print(c.getCost())

    c = Chromosome([[1, 1, 0, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 1], [0, 0, 1, 0, 1], [1, 0, 0, 0, 0], [0, 1, 0, 1, 1], [0, 1, 0, 0, 0], [1, 0, 1, 0, 0], [0, 0, 0, 0, 1], [0, 1, 0, 1, 0]])
    assert c.getCost() == 9.6    
    print(c.getCost())


    c = Chromosome([[1, 0, 1, 1, 1], [1, 1, 0, 0, 1], [1, 1, 0, 1, 1], [0, 1, 0, 1, 1], [1, 1, 0, 0, 0], [0, 1, 1, 1, 0], [1, 1, 0, 0, 1], [0, 1, 1, 0, 1], [0, 1, 1, 1, 0], [0, 1, 0, 0, 1]])
    assert c.getCost() == 60    
    print(c.getCost())

    c = Chromosome([[1, 1, 1, 1, 1], [0, 0, 0, 1, 0], [1, 1, 0, 0, 1], [1, 1, 1, 0, 1], [0, 1, 1, 0, 1], [0, 1, 0, 1, 0], [1, 0, 0, 1, 0], [0, 1, 0, 0, 1], [0, 0, 0, 0, 0], [1, 0, 0, 0, 0]])
    assert c.getCost() == 29.6
    print(c.getCost())
