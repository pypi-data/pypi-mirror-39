from setuptools import setup, find_packages


setup(
    name='hurlers',
    version='0.1.1',
    description='Store mlbam pitch data.',
    author='S.J. Browne',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords=['baseball', 'MLB', 'MLBAM', 'SABRmetrics', 'SABR', 'Major League Baseball', 'pitch', 'pitching'],
    license='MIT License',
    install_requires=[
        'bs4',
        'lxml',
        'requests',
    ],
    url='https://github.com/sjbrowne/hurlers',
    python_requires=">=2.7"
)
