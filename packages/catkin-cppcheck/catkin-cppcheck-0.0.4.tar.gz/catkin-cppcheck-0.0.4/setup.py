import os
from setuptools import setup, find_packages

root = os.path.dirname(os.path.realpath(__file__))
readme = os.path.join(root, 'README.rst')

setup(
    name='catkin-cppcheck',
    version='0.0.4',
    author='Natesh Narain',
    author_email='nnaraindev@gmail.com',
    description='Run cppcheck on catkin packages',
    long_description=open(readme).read(),
    license='MIT',
    keywords='catkin ros cppcheck c++',

    package_dir={'': 'src'},
    packages=['catkin_cppcheck'],

    install_requires=['catkin_pkg'],

    entry_points= {
        'catkin_tools.commands.catkin.verbs': [
            'cppcheck = catkin_cppcheck.main:description'
        ]
    }
)
