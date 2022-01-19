from setuptools import setup

setup(
    name = 'mailscan',
    version = '0.1.0',
    packages = ['mailscan'],
    entry_points = {
        'console_scripts': [
            'mailscan = mailscan.__main__:main'
        ]
    })

