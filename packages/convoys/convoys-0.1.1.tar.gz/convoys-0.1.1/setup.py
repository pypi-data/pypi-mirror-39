from setuptools import setup, find_packages

setup(name='convoys',
      version='0.1.1',
      description='Fit machine learning models to predict conversion using Weibull and Gamma distributions',
      url='https://better.engineering/convoys',
      license='MIT',
      author='Erik Bernhardsson',
      author_email='erikbern@better.com',
      packages=find_packages(),
      install_requires=[line.strip() for line in open('requirements.txt')])
