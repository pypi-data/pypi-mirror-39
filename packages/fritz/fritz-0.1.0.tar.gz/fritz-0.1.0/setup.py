# pylint: disable=missing-docstring
from setuptools import setup
from setuptools import find_packages

setup(name='fritz',
      version='0.1.0',
      description='Fritz Machine Learning Library.',
      url='https://github.com/fritzlabs/fritz-python',
      author='Chris Kelly',
      author_email='chris@fritz.ai',
      license='MIT',
      zip_safe=False,
      packages=find_packages(),
      install_requires=[
          'requests',
      ],
      extras_require={
          'keras': ['keras', 'tensorflow'],
      })
