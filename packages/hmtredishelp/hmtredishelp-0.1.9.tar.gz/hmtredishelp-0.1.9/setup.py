from setuptools import setup

setup(name='hmtredishelp',
      version='0.1.9',
      description='A set of tools we use to easily access redis',
      url='https://github.com/IntuitionMachines/redis-tools',
      author='Intuition Machines',
      author_email='dev@intuitionmachines.com',
      license='MIT',
      packages=['hmtredishelp'],
      install_requires=["redis==2.10.6"],
      zip_safe=False)

