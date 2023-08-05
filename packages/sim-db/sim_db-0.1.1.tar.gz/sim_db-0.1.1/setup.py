import setuptools

setuptools.setup(
    name='sim_db',
    version='0.1.1',
    scripts=['sim_db/sim_db', 'sim_db/sdb', 'sim_db/sim_db_cd.sh'],
    author='Hakon Austlid Tasken',
    author_email='hakon.tasken@gmail.com',
    description='A database for simulation parameters.',
    long_description='A command line tool and set of functions for conveniently running a large number of simulations with different parameter values, while keeping track of these all simulation parameters and results along with metadata in a database for you.',
    url='http://sim-db.readthedocs.io',
    packages=setuptools.find_packages(),
    classifiers=[
     "Programming Language :: Python",
     "Programming Language :: Python :: 2",
     "Programming Language :: Python :: 3",
     "Programming Language :: Python",
     "License :: OSI Approved :: MIT License",
    ],
    include_package_data=True,
)
