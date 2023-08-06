from setuptools import setup

setup(name='atman-logging-config',
      version='0.1',
      description='Logger with request id',
      url='',
      author='Atman Corp',
      author_email='corp@atman360.com',
      license='MIT',
      packages=['logging_config'],
      install_requires=[
          'flask-log-request-id>=0.10.0',
          'flask>=0.10.1',
          'python-json-logger>=0.1.10'
      ]
      )
