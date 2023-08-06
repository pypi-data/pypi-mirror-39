from setuptools import setup

setup(
    name='partial-apply',
    version='1.0.0',
    description='Partial application of functions and method names, supporting '
                'placeholder values for positional arguments.',
    long_description=open('README.rst').read(),
    url='https://github.com/crowsonkb/partial-apply',
    author='Katherine Crowson',
    author_email='crowsonkb@gmail.com',
    license='MIT',
    packages=['partial_apply'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords=['functional', 'higher-order', 'partial'],
)
