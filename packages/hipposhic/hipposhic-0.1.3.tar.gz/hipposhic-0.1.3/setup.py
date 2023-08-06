from setuptools import setup, find_packages

setup(name='hipposhic',
      version='0.1.3',
      description='my first upload to pyPI',
      url='https://github.com/jgallowa07/hipposhic.git',
      author='Jared Galloway',
      author_email='jaredgalloway07@gmail.com',
      license='MIT',      
      packages=find_packages(exclude=[]),
      scripts=['hipposhic/exampleScript'],
      install_requires=['numpy'],
      zip_safe=False,
      extras_require={
          'dev': [],
      },
      setup_requires=[],
      )

