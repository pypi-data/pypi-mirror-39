# Parallelic
Parallelic is a hyperparallel multi-node task execution engine with shared data and wokspace capabilities.

## Note of warning
Parallelic is not a containerization/sandboxing engine. It does not constitute a full task isolation, and provides no guarantee of such. That may change in the future, and feel free to contribute your code towards that goal, but in the mean time, keep this in consideration when giving access to a Parallelic system to third parties.

## Installation
### From git
  1. Clone the git repo locally.
  2. Download python3(.7) and corresponding pip
  3. Install [Poetry](https://poetry.eustace.io)
  4. Run `poetry install` to create a virtualenv and install dependencies  
  At this point, you can use parallelic through   
  `poetry run python -m parallelic`
  5. Run `poetry build` to build a wheel
  6. Run `pip install dist/parallelic-[version]-py3-none-any.whl`  
  Now you can use parallelic without poetry:  
  `python -m parallelic`
### From pip
  1. Run `pip install parallelic`

## Usage
### Running a task
To run an already defined task, you upload the task package (a zipped up task root directory) via the Parallelic WebUI, or Parallelic CLI client, to the Parallelic manager instance.   
You may need to provide access credentials before being allowed to upload the task package, as per your Parallelic system configuration.  
From there, the Parallelic manager instance will take care of everything else.
### Defining a task
Task definitions follow a particullar directory tree.  
The task root contains a `task.yml` file, that contains metadata required for the manager to set up and prepare resources for the compute nodes in order to run the particullar task.  

The `source` directory gets distributed to all compute nodes, it should contain only the source files required to run the task.  
This directory is set up with Read+eXecute permissions. Every task has to contain this directory.

The `data` directory gets distributed to all compute nodes, if `"shared_data"` is requested in the task's configuration. It is set up with Read+Write permissions.  
It is suitable for datasets that need to be shared across all nodes, but whose modifications by the nodes shouldn't propagate to other nodes. A task should contain this directory if `"shared_data"` is requested.  
It can be accessd by the task in the task's working directory.

The `workspace` directory gets created automatically by the manager, if `"shared_workspace"` is requested in the task's configuration.  
It is set up with Read+Write permissions, but `task.yml` can request the manager to create a `scripts` subdirectory, with Read+Write+eXecute permissions.  
It should never be in the task's root directory, and any content from the task's root directory won't get sent to the compute nodes. Compute nodes should populate this directory themselves, at runtime. Any changes to this directory will propagate across all compute nodes, and it can be access in the task's working directory.