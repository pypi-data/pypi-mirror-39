from setuptools import setup, find_packages

setup(
    name='catkin-cppcheck',
    version='0.0.1',
    author='Natesh Narain',
    author_email='nnaraindev@gmail.com',
    description='Run cppcheck on catkin packages',
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
