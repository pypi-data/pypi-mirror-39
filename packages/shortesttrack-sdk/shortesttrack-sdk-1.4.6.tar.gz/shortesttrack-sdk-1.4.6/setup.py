from setuptools import setup, find_packages

setup(
    name='shortesttrack-sdk',
    version='1.4.6',
    description='SDK for work with ShortestTrack API',
    packages=find_packages(),
    install_requires=[
        'URLObject==2.4.3',
        'requests==2.19.1',
        'shortesttrack-tools>=0.1.10,<0.2',
        'Faker==1.0.0',
        'funcy==1.11'
    ],
    author='Shortest Track',
    author_email='mpyzhov@shtr.io',
    license='MIT'
)
