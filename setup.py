from setuptools import setup

setuptools.setup(
    name='ndtest',
    version='0.1.0',
    packages=['ndtest'],
    entry_points={
    'console_scripts': [
        'ndtest = ndtest.__main__:main'
    ]
})
