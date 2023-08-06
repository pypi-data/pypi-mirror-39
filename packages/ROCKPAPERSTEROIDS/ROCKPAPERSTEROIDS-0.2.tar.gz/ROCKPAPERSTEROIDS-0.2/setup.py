from setuptools import setup, setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(name='ROCKPAPERSTEROIDS',
      version='0.2',
      description='an extended game of rock paper scissor ',      
      author = 'Thomas Musson',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/MUSSONT/ROCKPAPERSTEROIDS",
      packages=setuptools.find_packages(),      
      zip_safe=False)