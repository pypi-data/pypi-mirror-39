from setuptools import setup

setup(
   name='arxivtorm',
   version='0.1',
   description='Gets papers from ArXiv and puts them on your remarkable',
   author='Naren Dasan',
   author_email='naren@narendasan.com',
   license="NCSA",
   long_description="Make sure to install https://github.com/juruen/rmapi",
   packages=['arxivtorm'],
   install_requires=['arxiv'],
   entry_points = {
              'console_scripts': [
                  'arxivtorm = arxivtorm.main:main',                  
              ],              
          },
)