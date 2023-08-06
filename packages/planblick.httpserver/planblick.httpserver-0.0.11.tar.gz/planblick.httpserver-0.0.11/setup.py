from setuptools import setup
setup(name='planblick.httpserver',
      version='0.0.11',
      description='A simple class glueing together cherrypi and flask ina streamlined fashion',
      url='https://www.planblick.com',
      author='Florian Kröber @ Planblick',
      author_email='fk@planblick.com',
      license='MIT',
      packages=['planblick.httpserver'],
      install_requires=[
          'cherrypy',
      ],
      zip_safe=False)
