import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='baroque',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'jsonschema==2.6.0,<3.0',
        'pytz==2016.10',
        'PyYAML==3.12,<4.0',
        'requests==2.9.1,<3.0'
    ],
    test_suite='tests',
    license='MIT License',
    description='Baroque is an event brokering framework with a honey-sweet '
                'interface.',
    url='https://github.com/baroquehq/baroque',
    author='Claudio Sparpaglione',
    author_email='csparpa@gmail.com',
    classifiers=[
      "License :: OSI Approved :: MIT License",
      'Programming Language :: Python :: 3 :: Only',
      "Natural Language :: English",
      "Operating System :: OS Independent",
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "Topic :: Software Development :: Libraries",
      "Topic :: Communications"],
)
