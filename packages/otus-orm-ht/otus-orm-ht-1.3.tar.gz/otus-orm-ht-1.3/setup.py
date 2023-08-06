from setuptools import setup, find_packages

setup(name='otus-orm-ht',
      version='1.3',
      description='ORM with basic functions',
      long_description='ORM with basic functions like INSERT, UPDATE, etc.',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6'
      ],
      keywords='ORM OTUS',
      url='https://github.com/MyHardWay/Otus_Homework/tree/master/homework_5',
      author='MyHardWay',
      author_email='',
      packages=find_packages(),
      install_requires=[
          'markdown',
          'pysqlite3 '
      ],
      include_package_data=True,
      zip_safe=False)