#!/usr/bin/env python3

import fiend as my_pkg
from setuptools import setup, find_packages, Command
import os
import subprocess
import re
import sys

from sphinx.setup_command import BuildDoc

cmdclass = {'build_sphinx': BuildDoc}


class BuildDockerCommand(Command):

    """Class for building the docker image for fiend"""

    description = 'Build Docker image for ' + my_pkg.__name__
    user_options = []

    dockerfile_path = 'docker/Dockerfile'
    imagename = 'fiend'

    def initialize_options(self):
        # https://stackoverflow.com/a/9350788
        self.path = os.path.dirname(os.path.realpath(__file__))

        # Get git commit hash
        try:
            result = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                    stdout=subprocess.PIPE)
            self.githash = str(result.stdout, encoding='utf-8').strip('\n')
        except Exception as e:
            print("Obtaining git hash failed due to " + str(e))
            self.githash = None

        # Check if current git commit corresponds to a tag, make note of that
        # too
        try:
            result = subprocess.run(["git", "describe", "--exact-match",
                                     "--tags", "HEAD"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            p = re.match(r'^(?!fatal)(?P<tag>.*)\n?',
                         str(result.stdout, encoding='utf-8'))

            if p:
                self.gittag = p.group('tag')
            else:
                self.gittag = None
        except Exception as e:
            print("Obtaining git tag failed due to " + str(e))
            self.gittag = None

    def finalize_options(self):
        # Check that Docker command exists
        try:
            subprocess.run(["docker"], check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        except Exception as e:
            print("Docker command not found, exiting...")
            exit(1)

        if self.githash:
            print("Building Docker image from git commit: " + self.githash)
        if self.gittag:
            print("    ... aka git tag: " + self.gittag)

    def run(self):

        try:
            result = subprocess.run(["docker", "build", "-f",
                                     self.path+"/"+self.dockerfile_path, "."], check=True,
                                    stdout=subprocess.PIPE)
            lastline = str(result.stdout, encoding='utf-8').split('\n')[-2]
            p = re.match(r"Successfully built (?P<imageid>\w*)", lastline)
            if p:
                imageid = p.group('imageid')
                subprocess.run(["docker", "tag", imageid, self.imagename])
                if self.githash:
                    subprocess.run(["docker", "tag", imageid,
                                    self.imagename+":"+self.githash])
                if self.gittag:
                    subprocess.run(["docker", "tag", imageid,
                                    self.imagename+":"+self.gittag])

                subprocess.run(["docker", "tag", imageid, self.imagename])
        except Exception as e:
            print("Docker build failed with error: " + str(e))


class BuildDevDockerCommand(BuildDockerCommand):

    """ Class for building Docker image for the development of fiend """

    dockerfile_path = 'docker/Dockerfile_development'
    imagename = 'fiend-dev'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class MypyCommand(Command):

    """ Class for running the MYPY static type checker on fiend """

    description = 'Runs the MYPY static type checker on ' + my_pkg.__name__
    user_options = []

    def initialize_options(self):
        ...

    def finalize_options(self):
        ...

    def run(self):
        import mypy.api
        mypy.api.run(['-p', 'fiend', '--ignore-missing-imports'])

if sys.argv[1] != "test":
    install_requires=['numpy',
                        'scipy',
                        'matplotlib',
                        'h5py',
                        'mpi4py',
                        'petsc4py',
                        'slepc4py',
                        'fenics_dolfin',
                        'mshr',
                        'psutil',
                        'progressbar2',
                        'mypy'],
else:
    install_requires=[]

setup(name=my_pkg.__name__,
      author=my_pkg.__author__,
      author_email=my_pkg.__author_email__,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Physics'
      ],
      cmdclass={
          'build_docker': BuildDockerCommand,
          'build_dev_docker': BuildDevDockerCommand,
          'mypy': MypyCommand,
      },
      data_files=[('demos/hhg', ['demos/hhg/run.sh', 
                                 'demos/hhg/run_dev.sh',
                                 'demos/hhg/laser']),
                  ('demos/nanotip', ['demos/nanotip/1_near_field.py',
                                     'demos/nanotip/2_tise.py',
                                     'demos/nanotip/3_prepare_tdse.py',
                                     'demos/nanotip/4_propagate.py',
                                     'demos/nanotip/plot_field.py',
                                     'demos/nanotip/geometry.py',
                                     'demos/nanotip/parameters.py',
                                     'demos/nanotip/laser'])
                 ],
      description="Finite element nanoscale dynamics",
      entry_points={
          'console_scripts': [
              'fiend_linpol_tise = fiend.lin_pol.solve_tise:tirun_main',
              'fiend_linpol_prepare_tdse = fiend.lin_pol.prepare_tdse:prepare_tdse_main',
              'fiend_linpol_propagate = fiend.lin_pol.propagate:linpol_propagate_main',
              'fiend_animate_density = fiend.analysis.animate_density:animate_density',
              'fiend_draw_acceleration = fiend.analysis.draw_acceleration:draw_dipole_acceleration',
              'fiend_draw_laser = fiend.analysis.draw_laser:draw_laser',
              'fiend_draw_mesh = fiend.analysis.draw_mesh:draw_mesh',
              'fiend_draw_norm = fiend.analysis.draw_norm:draw_norm',
              'fiend_draw_pes = fiend.analysis.draw_pes:compute_pes_main',
              'fiend_draw_shapshot = fiend.analysis.draw_snapshot:draw_snapshot',
              'fiend_draw_stationary_states = fiend.analysis.draw_stationary_states:draw_stationary_states',
              'fiend_draw_velocity = field.analysis.draw_velocity:draw_dipole_velocity'
          ]
      },
      keywords=['numerics',
                'FEM',
                'finite-element method',
                'quantum mechanics',
                'Schrödinger equation',
                'physics'],
      install_requires=install_requires,
      license=my_pkg.__license__,
      package_data={
          '': ['*mplparams'],
      },
      long_description=read('README.rst'),
      packages=find_packages(),
      python_requires='>=3.6',
      test_suite='nose2.collector.collector',
      tests_require=['nose2'],
      url='https://fiend.solanpaa.fi',
      version=my_pkg.__version__,
      zip_safe=True)
