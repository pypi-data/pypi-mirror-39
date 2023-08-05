# setup.py
from setuptools import setup

setup(
    name='robolearn',
    version='0.0.0',
    description='A Robot-Learning package: Robot reinforcement learning.',
    author="domingoesteban",
    author_email="mingo.esteban@gmail.com",
    maintainer="domingoesteban",
    maintainer_email="mingo.esteban@gmail.com",
    packages=['robolearn'],
    install_requires=[
        'gym',
        'numpy',
        'torch',
        'robolearn_gym_envs',
        'tqdm',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
