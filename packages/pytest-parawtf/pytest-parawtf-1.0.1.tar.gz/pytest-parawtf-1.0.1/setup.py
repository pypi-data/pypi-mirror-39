import setuptools


setuptools.setup(
    name='pytest-parawtf',
    description='Finally spell paramete?ri[sz]e correctly',
    long_description=open("README").read(),
    version='1.0.1',
    author='Floris Bruynooghe',
    author_email='flub@devork.be',
    url='http://bitbucket.org/flub/pytest-parawtf/',
    license='MIT',
    py_modules=['pytest_parawtf'],
    entry_points={'pytest11': ['parawtf = pytest_parawtf']},
    install_requires=['pytest>=3.6.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: DFSG approved',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
    ],
)
