from setuptools import setup, find_packages

setup(
    name='bouncer',
    version='0.0.4',
    description='Client for Bouncer A/B testing service',
    long_description=open('README.rst').read(),
    author='Robin Edwards',
    author_email='robin.ge@gmail.com',
    zip_safe=True,
    url='http://github.com/robinedwards/bouncerpy',
    license='MIT',
    packages=find_packages(),
    keywords='bouncer',
    install_requires=['requests==2.8.1'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Programming Language :: Python :: 2.7",
    ])
