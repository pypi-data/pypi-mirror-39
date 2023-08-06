from setuptools import setup, find_packages

setup(name='ssu_tk',

      version='0.0.0.1',

      url='https://github.com/jason9693/ssu_keras',

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
        'tensorflow >= 1.1.2'
      ],

      packages=find_packages(),

      description = 'support custom tf.keras modules bundle for tensorflow v2.x',

      zip_safe=False,

      )