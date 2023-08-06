import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='caddy',
    version='0.1.0',
    author='Radek Ježek, Dominika Králiková, Róbert Selvek, Jakub Topič',
    author_email='topicjak@fit.cvut.cz',
    url='https://gitlab.fit.cvut.cz/jezekra1/oop-semester-project',
    description='Semester project for OOP course',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities"
    ],

    include_package_data=True,
    entry_points={
        'console_scripts': [
            'caddy=caddy.main:main',
        ]
    },
    packages=setuptools.find_packages(),
    test_suite='nose.collector',
    tests_require=['nose', 'pylint', 'coverage', 'mock']
)
