from setuptools import setup, find_packages

setup(name='model_writer',

      version='0.0.0.2',

      url='https://github.com/jason9693/ModelWriter',

      long_description = open('./README.md').read(),

      license='MIT',

      author='Yang Kichang',

      author_email='ykcha9@gmail.com',

      python_requires = '>=3',

      classifiers=[

          'Development Status :: 4 - Beta',

          'Intended Audience :: Developers',

          'License :: OSI Approved :: MIT License',

          'Programming Language :: Python :: 3.6',

          'Programming Language :: Python :: 3.5',

          'Programming Language :: Python :: 3.4',

      ],

      install_requires=[
        'tabulate>=0.8.2',
        'pandas>=0.23.4',
      ],

      packages=find_packages(exclude=['test.csv']),

      description = 'Model Writer For ML training or test time',

      zip_safe=False,

      )