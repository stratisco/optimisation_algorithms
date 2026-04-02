class StaffMember:
    def __init__(self, id:int, available_hours:int, skill_level:int, skills:list[str]):
        self.id = id
        self.available_hours = available_hours
        self.skill_level = skill_level
        self.skills = skills

    def __str__(self):
        return f'S{self.id}'
    
    def __repr__(self):
        return f'S{self.id}({self.available_hours}, {self.skill_level}, {self.skills})'


class Project:
    def __init__(self, id:int, estimated_time:int, difficulty:int, deadline:int, required_skill:str):
        self.id = id
        self.estimated_time = estimated_time
        self.difficulty = difficulty
        self.deadline = deadline
        self.required_skill = required_skill

    def __str__(self):
        return f'P{self.id}'
    
    def __repr__(self):
        return f'P{self.id}({self.estimated_time}, {self.difficulty}, {self.deadline}, {self.required_skill})'


STAFF_LIST: list[StaffMember] = [
    StaffMember(1, 9,  5, ['A', 'C']),
    StaffMember(2, 10, 4, ['A', 'C']),
    StaffMember(3, 12, 6, ['A', 'B', 'C']),
    StaffMember(4, 8,  3, ['A']),
    StaffMember(5, 15, 7, ['B', 'C'])    
]


PROJECTS_LIST: list[Project] = [
    Project(1,  6, 4, 11, 'C'),
    Project(2,  4, 3, 8,  'A'),
    Project(3,  6, 5, 12, 'B'),
    Project(4,  2, 2, 6,  'A'),
    Project(5,  5, 4, 10, 'C'),
    Project(6,  3, 1, 7,  'A'),
    Project(7,  8, 6, 15, 'B'),
    Project(8,  4, 3, 9,  'C'),
    Project(9,  7, 5, 14, 'B'),
    Project(10, 2, 2, 5,  'A')    
]


STAFF_DICT: dict[int, StaffMember] = {s.id: s for s in STAFF_LIST}
PROJECTS_DICT: dict[int, Project] = {s.id: s for s in PROJECTS_LIST}


if __name__ == '__main__':
    print(STAFF_DICT)
    print(PROJECTS_DICT)