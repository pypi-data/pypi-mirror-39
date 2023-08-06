from distutils.core import setup


setup(
    name='browserly',
    packages=['browserly'],
    version='0.0.3',
    license='MIT',
    description='App browserly',
    author='xazrad',
    author_email='xazrad@gmail.com',
    url='https://github.com/xazrad/browserly',
    download_url='https://github.com/xazrad/browserly/archive/0.0.3.tar.gz',
    keywords=[],
    install_requires=[
        'click',
        'selenium'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    py_modules=['browserly'],
    extras_require={
        'test':[
            'tox',
            'pytest',
            'coverage'
        ]
    },
    entry_points={
        'console_scripts': [
            'browserly = browserly.cli:cli'
        ]
    },
)
