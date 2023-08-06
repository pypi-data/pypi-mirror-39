from setuptools import find_packages, setup

setup(
    name='rbx',
    version='1.1.2',
    license='Apache 2.0',
    description='Scoota Platform for the Rig',
    url='http://scoota.com/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Internet',
    ],
    zip_safe=True,
    author='The Scoota Engineering Team',
    author_email='engineering@scoota.com',
    python_requires='>=3.6',
    install_requires=[
        'click==6.7',
        'googlemaps==3.0.2',
    ],
    entry_points={
        'console_scripts': [
            'geocode = rbx.cli.geo:geocode',
            'unpack = rbx.cli.geo:unpack',
        ],
    },
    packages=find_packages(),
    namespace_packages=['rbx'],
)
