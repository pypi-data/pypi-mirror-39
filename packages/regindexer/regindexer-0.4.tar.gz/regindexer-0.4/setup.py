from setuptools import setup

setup(name='regindexer',
      version='0.4',
      description='fedmsg-hub plugin to maintain a static registry index',
      url='https://pagure.io/regindexer',
      author='Owen Taylor',
      author_email='otaylor@redhat.com',
      license='MIT',
      packages=['regindexer'],
      include_package_data=True,
      install_requires=[
          'click',
          'requests',
          'PyYAML',
      ],
      entry_points= {
          'console_scripts': [
              'regindexer=regindexer.cli:cli',
              'regindexer-daemon=regindexer.daemon:main',
          ],
      })
