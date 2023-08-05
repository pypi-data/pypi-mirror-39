from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='nanoid-dictionary',
    version='2.1.0',
    author='Dair Aidarkhanov',
    author_email='dairaidarkhanov@gmail.com',
    description='Predefined character sets to use with Nano ID',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/aidarkhanov/py-nanoid-dictionary',
    license='MIT',
    packages=['nanoid_dictionary'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ]
)
