from setuptools import setup

setup(
    name='pointpy',
    version='1.0.2',
    description='point client',
    author="@gyran",
    author_email="gustav.ahlberg@gmail.com",
    install_requires=[
        'requests>=2.20.1',
    ],
    license='LICENSE.txt',
    packages=['pointpy']
)
