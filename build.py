
import os
import subprocess

import pybuilder.core as pyb
import pybuilder.utils


pyb.use_plugin('python.core')
pyb.use_plugin('python.unittest')
pyb.use_plugin('python.install_dependencies')
pyb.use_plugin('python.coverage')
pyb.use_plugin('python.distutils')
pyb.use_plugin('python.pycharm')

pyb.use_plugin('filter_resources')
pyb.use_plugin('copy_resources')

name = 'gitpage'
default_task = 'publish'


@pyb.init
def set_properties(project):
    project.authors = [pyb.Author('Noah Davis', 'noahdavis319@gmail.com')]
    project.summary = 'GitPage - A Python-based Git web-app.'
    project.description = ('GitPage is a Python-based Git web-app that uses pygit2 and '
                           'Flask to provided a web interface similar to GitHub, GitLab, '
                           'BitBucket, and more!')

    project.depends_on('pygit2')
    project.depends_on('flask')

    project.set_property('coverage_threshold_warn', 85)
    project.set_property('coverage_branch_threshold_warn', 85)
    project.set_property('coverage_branch_partial_threshold_warn', 85)
    project.set_property('coverage_break_build', False)

    project.get_property("filter_resources_glob").append("**/gitpage/__init__.py")

    project.include_file('gitpage', 'resources/templates/*')


@pyb.task(description='Downloads and installs the libgit2 library.')
def install_libgit2(project, logger):
    """
    Download and install libgit2 which is required for pygit2 to successfully install.
    """
    logger.info('Installing libgit2')
    cmd = """cd {0}
        export LIBGIT2=$VIRTUAL_ENV
        wget --no-clobber https://github.com/libgit2/libgit2/archive/v0.27.0.tar.gz
        tar xzf v0.27.0.tar.gz
        cd libgit2-0.27.0/
        cmake . -DCMAKE_INSTALL_PREFIX=$LIBGIT2
        make
        make install
        rm -rf libgit2-0.27.0/
        """.format(project.expand('$dir_dist/dist'))
    run(project, logger, 'install_libgit2',
        cmd)


@pyb.task(description='Downloads and installs pygit2 manually due to being installed '
                      'into a virtual environment.')
@pyb.before('install_dependencies')
def install_pygit2(project, logger):
    """
    Install the pygit2 library using pip and setting installation environment variables.
    """
    logger.info('Installing pygit2')
    run(project, logger, 'install_pygit2',
        """export LDFLAGS="-Wl,-rpath=$VIRTUAL_ENV/lib,--enable-new-dtags $LDFLAGS"
        pip install pygit2
        """)


@pyb.task()
@pyb.depends('install_pygit2')
def install_dependencies():
    pass


@pyb.task()
@pyb.depends('install_dependencies')
def prepare():
    pass


def run(project, logger, cmd_name, command):
    """
    Run a command in a shell during a PyBuilder task saving the stdout and stderr to log
    files. If the command has a non-zero return code then this method raises an exception.
    """
    dir_logs = project.expand('$dir_logs')
    pybuilder.utils.mkdir(dir_logs)
    out_file = os.path.join(dir_logs, '{0}.log'.format(cmd_name))
    err_file = os.path.join(dir_logs, '{0}.err'.format(cmd_name))
    with open(out_file, 'w') as out:
        with open(err_file, 'w') as err:
            retcode = subprocess.call(command, shell=True, stdout=out, stderr=err)
            if retcode:
                logger.error("{2} failed. See {0} and {1} for details."
                             .format(out_file, err_file, cmd_name))
                raise Exception("{0} Failed".format(cmd_name))
