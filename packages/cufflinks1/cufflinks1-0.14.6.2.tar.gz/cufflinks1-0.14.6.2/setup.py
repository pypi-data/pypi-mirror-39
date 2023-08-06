from setuptools import setup
from os import path
import io

here = path.abspath(path.dirname(__file__))
with io.open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requires = f.read().split()

setup(name='cufflinks1',
      version='0.14.6.2',
      description='Productivity Tools for Plotly + Pandas, with refined default configuration',
      author='Cailiang Liu',
      author_email='cailiang.thu@gmail.com',
      license='MIT',
      keywords = ['pandas', 'plotly', 'plotting'],
      url = 'https://github.com/cailiang9/cufflinks',
      packages=['cufflinks'],
      package_data={'cufflinks': ['../helper/*.json']},
      include_package_data=True,
      install_requires=requires,
	  zip_safe=False)
