from setuptools import setup

setup(name='pypai',
      version='1.2',
      description='The python tool for Open Platform for AI',
      url='https://github.com/GeoffreyChen777/pypai',
      author='Geoffrey CHen',
      author_email='geoffreychen777@gmail.com',
      license='MIT',
      packages=['pypai'],
      zip_safe=False,
      install_requires=[
        'requests',
        'pyhdfs',
    ])
