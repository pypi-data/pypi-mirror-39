from setuptools import setup, find_packages


setup(
		name='ml-etl',
      	version='0.1.0.dev0',
	  	description='machine learning data pipeline',
	  	packages=find_packages(exclude=['tests']),
		url='http://10.0.1.31/ML/ml-storage/ml-etl/',
		author='henrychi',
		author_email='shyuusaku@gmail.com',
		license='Gogoro Inc.',
		keywords='ml',
        classifiers = [
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
		install_requires=[
			'boto3>=1.9.57',
			'configparser>=3.5.0',
			'ordereddict>=1.1',
			'pymongo>=3.7.2',
			'pyodbc>=4.0.24',
		]
)
