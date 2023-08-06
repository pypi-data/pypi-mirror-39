from setuptools import setup


setup(
    name='MultiscaleEntropy',
    version='0.0.1',
    description='A Python module to calculate Multiscale  Entropy of a time series.',
    url='https://github.com/reatank/MultiscaleEntropy',
    author='reatank',
    author_email='reatank@foxmail.com',
    maintainer='reatank',
    maintainer_email='reatank@foxmail.com',
    license='GNU',
    packages=['MultiscaleEntropy'],
    install_requires=[
        'numpy>=1.9.2',
    ],
    keywords=['multiscale entropy', 'mse']
)