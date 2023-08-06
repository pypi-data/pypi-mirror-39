import setuptools

setuptools.setup(
    name='pipns',
    author='Andrew Rabert',
    author_email='ar@nullsum.net',
    url='https://github.com/nvllsvm/pipns',
    license='MIT',
    packages=['pipns'],
    entry_points={'console_scripts': ['pipns=pipns:main']},
    package_data={'pipns': ['scripts/*.py']},
    install_requires=['pipenv'],
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    python_requires='>=3.7')
