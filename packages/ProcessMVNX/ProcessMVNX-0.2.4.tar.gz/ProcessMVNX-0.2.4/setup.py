from setuptools import setup, find_packages

with open('README') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name="ProcessMVNX",
    version="0.2.4",
    description = "Tool for reading and processing MVNX-Files from the"
                  " xsens-Awinda Motion Capturing System.",
    long_description = readme,
    url='https://gitlab.com/Benjamin_Knopp/ProcessMVNX',
    author="Benjamin Knopp",
    author_email='knoppbe@staff.uni-marburg.de',
    license='MIT',
    # packages = find_packages(),
    packages = find_packages(exclude=['tests']),
    install_requires = requirements,
    classifiers=[
           'Development Status :: 2 - Pre-Alpha',
           'Intended Audience :: Science/Research',
           'License :: OSI Approved :: MIT License',
           'Natural Language :: English',
           'Operating System :: POSIX :: Linux',
           'Programming Language :: Python :: 3',
           'Topic :: Utilities'
    ]
)
