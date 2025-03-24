# plcg

A package created by the Pardee Lab Computation Group containing a variety of python utilities which we have found useful in a variety of biology projects.

## Software requirements:

[Local Colabfold](https://github.com/YoshitakaMo/localcolabfold)

Must be in path such that the user can call colabfold_batch from inside terminal in which you are running the project

[pyrosetta](https://www.pyrosetta.org/)

Should be installed into it's own environment as it is not yet supported in python 3.11, and thus we take the conda path as a function argument


## Development model:

Workflows auto release new versions (Which are manually updated in [setup.py](https://github.com/Pardee-Lab-Computation-Group/plcg/blob/main/setup.py))

- Pushes to [main](https://github.com/Pardee-Lab-Computation-Group/plcg/tree/main) release to pypi.
- Pushes to [test-pypi](https://github.com/Pardee-Lab-Computation-Group/plcg/tree/test-pypi) release to test-pypi.

General practice is that we make pr (or push directly) to test-pypi first, pull it into a real project to test, and then pr to main. 

- If you don't want to release, simply don't update version and workflows will fail harmlessly.
- In the future we might update to only release when it finds the a change in setup.py version.
