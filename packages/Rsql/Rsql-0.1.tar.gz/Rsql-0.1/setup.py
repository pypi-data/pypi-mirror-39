from setuptools import setup, find_packages

setup(name='Rsql',
      version='0.1',
      description='Rsql',
      long_description='Really, the funniest around.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      author='Raf',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'PyMySQL==0.9.3',
      ],
      include_package_data=True,
      zip_safe=False)