import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='qc_utils',
    version='0.1',
    packages=setuptools.find_packages(),
    license='MIT',
    author='Otto Jolanki',
    author_email='ojolanki@stanford.edu',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/encode-dcc/qc-utils',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)