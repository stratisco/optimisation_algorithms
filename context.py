class StaffMember:
    def __init__(self, id:int, available_hours:int, skill_level:int, skills:list[str]):
        self.id = id
        self.available_hours = available_hours
        self.skill_level = skill_level
        self.skills = skills

    def __str__(self):
        return f'S{self.id}'


class Project:
    def __init__(self, id:int, estimated_time:int, difficulty:int, deadline:int, required_skill:str):
        self.id = id
        self.estimated_time = estimated_time
        self.difficulty = difficulty
        self.deadline = deadline
        self.required_skill = required_skill

    def __str__(self):
        return f'P{self.id}'
    


# must be in order of staff id
STAFF_LIST: list[StaffMember] = [
    StaffMember(0, 9,  5, ['A', 'C']),
    StaffMember(1, 10, 4, ['A', 'C']),
    StaffMember(2, 12, 6, ['A', 'B', 'C']),
    StaffMember(3, 8,  3, ['A']),
    StaffMember(4, 15, 7, ['B', 'C'])    
]


# must be in order of project id
PROJECTS_LIST: list[Project] = [
    Project(0, 6, 4, 11, 'C'),
    Project(1,  4, 3, 8,  'A'),
    Project(2,  6, 5, 12, 'B'),
    Project(3,  2, 2, 6,  'A'),
    Project(4,  5, 4, 10, 'C'),
    Project(5,  3, 1, 7,  'A'),
    Project(6,  8, 6, 15, 'B'),
    Project(7,  4, 3, 9,  'C'),
    Project(8,  7, 5, 14, 'B'),
    Project(9,  2, 2, 5,  'A')    
]
