from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pandan',
      version='0.1',
      description='A small library to make decisions out of sequences of evidences',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
      ],
      keywords='sequential decision making',
      url='https://github.com/zebehn/pandan.git',
      author='Minsu Jang',
      author_email='minsu@etri.re.kr',
      license='BSD 3-Clause',
      packages=['pandan'],
      install_requires=[
      ],
      include_package_data=True,
      zip_safe=False)