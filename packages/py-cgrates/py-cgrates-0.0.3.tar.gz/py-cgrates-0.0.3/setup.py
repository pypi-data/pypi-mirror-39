from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(name='py-cgrates',
      description='Py CGRrateS',
      long_description=long_description,
      long_description_content_type="text/markdown",
      version='0.0.3',
      url='https://github.com/hampsterx/py-cgrates',
      author='Tim van der Hulst',
      author_email='tim.vdh@gmail.com',
      license='GNU General Public License v3.0',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python :: 3'
      ],
      packages=find_packages(exclude=["tests"]),
      install_requires=[
        'marshmallow==3.0.0rc1'
      ]
)