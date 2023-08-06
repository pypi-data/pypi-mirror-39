from setuptools import setup

setup(name='savemodel',
      version='0.1',
      description='To save models to HDFS',
      url='http://github.com',
      author='Yogesh Somawar',
      author_email='yogesh.somawar@qio.io',
      license='MIT',
      packages=['savemodel'],
      install_requires=[
	'clipper_admin',
	'pyspark',
	'tensorflow',
	'keras',
	'h2o'
      ],
      zip_safe=False)
