import setuptools

setuptools.setup(
    name='easy-parse',
    version='0.1.0',
    python_requires='>=3.6',
    packages=setuptools.find_packages(exclude=['*.tests', '*.data']),
    install_requires=[],
    license='MIT',
    description='Easy parsing for xml and json',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Colton Willig',
    author_email='coltonwillig@gmail.com',
    url='https://github.com/uncmath25/easy-parse'
)
