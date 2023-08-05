
from setuptools import setup, find_packages

setup(name='universal_response_mobile_api',
      version='0.1.1',
      description='Add universal response for your API',
      long_description='Add universal response for your API.',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      keywords='api mobile response',
      url='https://bitbucket.org/anmv/universal-response-mobile-api',
      author='Damir, Alexandr',
      author_email='exorciste.2007@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'Django>=2.0', 'djangorestframework>=3.8.2'
      ],
      include_package_data=False,
      zip_safe=False)