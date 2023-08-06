from setuptools import setup, find_packages

with open('README.md') as infile:
	readme = infile.read()

setup(
    name='xuebadb',
    version='1.2',
    python_requires='>=3',
    packages= find_packages(exclude=['tests*']),
    install_requires=['mysql-connector-python', 'pandas', 'pyodbc', 'numpy', 'missingno', 'seaborn', 'matplotlib'],
    license='MIT',
    description='xuebadb is a python package that allows users to conveniently connect to and query from various database systems using a unified API. Currently, it supports connecting to MySQL and SQL Server database systems. The queries return Pandas dataframes which can then be cleaned up and analysed using one of the modules in the package.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url ='https://github.com/ubco-mds-2018-labs/data533_lab4_vaghul_jiachen',
    author='Vaghul Aditya Balaji',
    author_email ='vaghulb1992@gmail.com' 
)