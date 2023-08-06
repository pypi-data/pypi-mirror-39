# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['parallelic', 'parallelic.comms', 'parallelic.manager', 'parallelic.runner']

package_data = \
{'': ['*']}

install_requires = \
['pytest-cov>=2.6,<3.0', 'pyzmq>=17.1,<18.0']

entry_points = \
{'console_scripts': ['parallelic = parallelic:main']}

setup_kwargs = {
    'name': 'parallelic',
    'version': '0.1.2',
    'description': 'Hyper-parallel multi-node task execution engine',
    'long_description': '# Parallelic\nParallelic is a hyperparallel multi-node task execution engine with shared data and wokspace capabilities.\n\n## Note of warning\nParallelic is not a containerization/sandboxing engine. It does not constitute a full task isolation, and provides no guarantee of such. That may change in the future, and feel free to contribute your code towards that goal, but in the mean time, keep this in consideration when giving access to a Parallelic system to third parties.\n\n## Installation\n### From git\n  1. Clone the git repo locally.\n  2. Download python3(.7) and corresponding pip\n  3. Install [Poetry](https://poetry.eustace.io)\n  4. Run `poetry install` to create a virtualenv and install dependencies  \n  At this point, you can use parallelic through   \n  `poetry run python -m parallelic`\n  5. Run `poetry build` to build a wheel\n  6. Run `pip install dist/parallelic-[version]-py3-none-any.whl`  \n  Now you can use parallelic without poetry:  \n  `python -m parallelic`\n### From pip\n  1. Run `pip install parallelic`\n\n## Usage\n### Running a task\nTo run an already defined task, you upload the task package (a zipped up task root directory) via the Parallelic WebUI, or Parallelic CLI client, to the Parallelic manager instance.   \nYou may need to provide access credentials before being allowed to upload the task package, as per your Parallelic system configuration.  \nFrom there, the Parallelic manager instance will take care of everything else.\n### Defining a task\nTask definitions follow a particullar directory tree.  \nThe task root contains a `task.yml` file, that contains metadata required for the manager to set up and prepare resources for the compute nodes in order to run the particullar task.  \n\nThe `source` directory gets distributed to all compute nodes, it should contain only the source files required to run the task.  \nThis directory is set up with Read+eXecute permissions. Every task has to contain this directory.\n\nThe `data` directory gets distributed to all compute nodes, if `"shared_data"` is requested in the task\'s configuration. It is set up with Read+Write permissions.  \nIt is suitable for datasets that need to be shared across all nodes, but whose modifications by the nodes shouldn\'t propagate to other nodes. A task should contain this directory if `"shared_data"` is requested.  \nIt can be accessd by the task in the task\'s working directory.\n\nThe `workspace` directory gets created automatically by the manager, if `"shared_workspace"` is requested in the task\'s configuration.  \nIt is set up with Read+Write permissions, but `task.yml` can request the manager to create a `scripts` subdirectory, with Read+Write+eXecute permissions.  \nIt should never be in the task\'s root directory, and any content from the task\'s root directory won\'t get sent to the compute nodes. Compute nodes should populate this directory themselves, at runtime. Any changes to this directory will propagate across all compute nodes, and it can be access in the task\'s working directory.',
    'author': 'golyalpha',
    'author_email': 'golyalpha@gmail.com',
    'url': 'https://gitlab.com/OnDev-Project/parallelic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
