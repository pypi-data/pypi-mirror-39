from setuptools import setup, find_packages

setup(name='flask-turn-apigateway',
      version='0.1.1',
      description='for develop apigateway',
      url='https://github.com/StevenLianaL/turnflaskrestfulapigateway',
      author='wz',
      author_email='wangzhou8284@163.cm',
      packages=find_packages(),
      zip_safe=False,
      python_requires='>=3.6',
      install_requires=['pyjwt', 'PyMySQL'],
      test_requires=[
      ])
