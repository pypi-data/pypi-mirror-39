import os

from setuptools import setup, find_packages

from distutils.core import Command

from setuptools.command.sdist import sdist as SDistCommand
from setuptools.command.develop import develop as DevelopCommand


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'xoutil>=1.9.9,<2.0;python_version<"3.0"',
    'xoutil>=1.9.9;python_version>="3.0"',
    'requests>=2.3.0,<2.4',
]

server_requires = [
    'pyramid>=1.5,<1.6',
    'pyramid_jinja2>=1.3,<1.4',
    'pyramid_tm',
    'pyramid_storage>=0.1.0',
    'SQLAlchemy>=1.2,<1.3',
    'transaction',
    'zope.sqlalchemy',
    'PasteDeploy>=1.5,<1.6',
]


testing_requires = server_requires + [
    'pyramid_debugtoolbar>=2.0.2,<2.1',
    'pyramid_mako',
    'devmail',
    'nose',
    'coverage',
    'waitress',
]


class XakoSDistCommand(SDistCommand):
    # If we are not a light build we want to also execute build_assets as
    # part of our source build pipeline.
    sub_commands = SDistCommand.sub_commands + [('build_assets', None)]


class XakoDevelopCommand(DevelopCommand):
    def run(self):
        DevelopCommand.run(self)
        self.run_command('build_assets')


class BuildAssetsCommand(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if os.system('make'):
            raise RuntimeError


cmdclass = {
    'sdist': XakoSDistCommand,
    'develop': XakoDevelopCommand,
    'build_assets': BuildAssetsCommand,
}


setup(name='xako',
      version='0.7.0',
      description='Remote file transfer micro-application.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Merchise Autrement',
      author_email='',
      url='',
      keywords=('file transfer'),
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      extras_require={
          'client': [],  # Just to allow install "xako[client]"
          'server': server_requires,
          'testing': testing_requires,
      },
      cmdclass=cmdclass,
      entry_points="""\
      [paste.app_factory]
      main = xako:main
      [console_scripts]
      initialize_xako_db = xako.scripts.initializedb:main
      xako_transmit_documents = xako.scripts.messages:transmit_documents
      xako_transmit_ctrlmsgs = xako.scripts.messages:transmit_control_messages
      xako_remove_documents = xako.scripts.messages:remove_old_documents
      xako_clean = xako.scripts.clean:clean
      xako_print_fingerprint = xako.scripts.utils:print_fingerprint
      """,
      )
