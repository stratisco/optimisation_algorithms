> [!IMPORTANT]
> Make sure you have pulled before you make a pull request to try avoid merge conflicts

## Vector representation *(for genetic algorithm)*:

uses a 3d vector of bits such that `vector[projectId][staffId]` equals `1` if the staff member is assigned to the project and `0` if not

```
# example with 4 projects and 5 staff members

vector = [
    [0, 1, 0, 0, 0],   # Project 1 -> Staff 2
    [0, 1, 0, 1, 0],   # Project 2 -> Staff 2, Staff 4 (over assigned)
    [1, 0, 0, 0, 0],   # Project 3 -> Staff 1
    [0, 0, 0, 0, 0],   # Project 4 -> (under assigned)
]
```


## Files

*misc scripts*
* `main.py` - main script to run all programs
* `context.py` - context for situation (staff/project info)

*genetic algorithm*
* `genetic.py` - main genetic algorithm script
* `chromosome.py` - chromosome/vector script

*particle swarm*
* `particle.py` - 
* `swarm.py` - 


<!-- *outputs*
* `genetic_graph.png` - graphical output showing the cost over each generation
* `cost_distribution.png` - small graph to show distribution of random assignment vectors -->

*misc*
* `README.md` - this file
* `.gitignore` - git ignore file


## Running this script
1. Clone repo
2. Navigate to base directory
3. Run `python main.py`
4. See output and note that now `genetic_graph.png` is now generated