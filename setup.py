from setuptools import setup

setup(name='MapMate',
      version='0.1',
      description='Library used for creating 2/3D world maps of data',
      url='https://github.com/AoifeHughes/MapMate',
      author='Aoife Hughes',
      author_email='Aoife.hughes@jic.ac.uk',
      license='MIT',
      packages=['MapMate'],
      install_requires=['numpy',
                        'pandas',
                        'pycountry',
                        'plotly',
                        'tqdm'],
      
      zip_safe=True)