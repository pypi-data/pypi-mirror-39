from setuptools import find_packages, setup

setup(
    name='hellokitty',
    version='0.0.3',
    description='Some funny app!',
    author='Mindey',
    author_email='mindey@qq.com',
    url='https://github.com/mindey/hellokitty',
    packages = find_packages(exclude=['docs', 'tests*']),
)
