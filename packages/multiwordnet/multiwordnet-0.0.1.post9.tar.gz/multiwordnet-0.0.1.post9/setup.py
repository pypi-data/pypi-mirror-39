from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='multiwordnet',
      version='0.0.1.post9',
      description='A helper library for accessing and manipulating WordNets in the MultiWordNet',
      long_description=long_description,
      url='',
      author='William Michael Short',
      author_email='w.short@exeter.ac.uk',
      license='Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)',
      packages=['multiwordnet', 'multiwordnet.db'],
      python_requires='>=3.5',
      install_requires='tqdm',
      package_data={
        'multiwordnet': ['db/*/*.sql'],
      },
      include_package_data=True,
      zip_safe=False)