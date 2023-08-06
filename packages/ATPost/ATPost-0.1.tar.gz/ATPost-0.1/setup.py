from setuptools import setup, find_packages
 
setup(name='ATPost',
      version='0.1',
      author='Shivanshu Choudhary',
      author_email='shivansh99choudhary@gmail.com',
      description='ATcommands ',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)