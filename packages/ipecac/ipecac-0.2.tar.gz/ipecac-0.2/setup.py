from setuptools import setup, find_packages

setup(
    name='ipecac',
    version='0.2',
    description='Generate Swagger/OAS 3.0 documentation from Python comments',
    author='Marcus Crane',
    author_email='marcus@utf9k.net',
    packages=find_packages(),
    install_requires=['click', 'PyYAML'],
    entry_points={
        'console_scripts': ['ipecac=ipecac.cli:create'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities',
    ]
)
