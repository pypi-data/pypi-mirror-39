from setuptools import setup, find_packages 

with open('README.md') as f:
    long_description = f.read()

setup(name='divinegift',
      version='0.9.5',
      description='It is a Divine Gift',
      long_description=long_description,
      long_description_content_type='text/markdown',  # This is important!
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3',
                   "Operating System :: OS Independent", ],
      keywords='s7_it',
      url='https://github.com/Malanris/DivineGift.git',
      author='Malanris',
      author_email='admin@malanris.ru',
      license='MIT',
      packages=find_packages(),
      install_requires=['sqlalchemy', 'requests', 'mailer'],
      include_package_data=True,
      zip_safe=False)