import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
      name='instagram_grabber',
      version='1.2',
      description='Tool for grabbing profile data, Instagram ID, block users and more...',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/Aspoky/instagram_grabber/',
      author='Aspoky',
      author_email = '',
      license='MIT',
      packages=['instagram_grabber'],
      install_requires=[
          'selenium>=3.14.1',
          'fake_useragent>=0.1.11',
      ],
      python_requires='>=3.6.0',
      zip_safe=False)