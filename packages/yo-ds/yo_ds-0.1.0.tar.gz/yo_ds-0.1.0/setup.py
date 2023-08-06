from setuptools import setup, find_packages


setup(name='yo_ds',
      version='0.1.0',
      description='The funnctional tools mostly for data science',
      url='http://google.com',
      author='Yuri Okulovsky',
      author_email='yuri.okulovsky@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            'pandas'
      ],
      zip_safe=False)