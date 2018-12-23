from setuptools import setup

setup(
    name = 'rocketload',
    version = '0.1.0',
    packages = ['rocketload'],
    entry_points = {
        'console_scripts': [
            'rocketload = rocketload.__main__:main'
        ]
    })

