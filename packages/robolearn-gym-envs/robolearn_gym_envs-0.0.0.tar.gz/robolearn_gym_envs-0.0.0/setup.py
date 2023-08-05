from setuptools import setup

setup(
    name='robolearn_gym_envs',
    version='0.0.0',
    description="A python package that contains some OpenAIGym-like robot "
                "environments.",
    maintainer="Domingo Esteban",
    packages=['robolearn_gym_envs'],
    install_requires=[
        'gym',
        'pybullet',
        'numpy',
        'transforms3d',
        'sympy',  # Because transforms3d doesn't install it
    ],
)

