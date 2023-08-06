from setuptools import setup, find_packages

def readme():
      with open('README.rst') as file:
            return file.read()

setup(name='yo_ds',
      version='0.1.1',

      description='The toolkit for data science projects with a focus on functional programming',
      long_description=readme(),
      classifiers = [
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      url='http://comingsoon.com',
      author='Yuri Okulovsky',
      author_email='yuri.okulovsky@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            'pandas'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data = True,
      zip_safe=False)