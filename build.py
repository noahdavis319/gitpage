
import os
import subprocess

import pybuilder.core as pyb
import pybuilder.utils


pyb.use_plugin('python.core')
pyb.use_plugin('python.unittest')
pyb.use_plugin('python.install_dependencies')
pyb.use_plugin('python.flake8')
pyb.use_plugin('python.coverage')
pyb.use_plugin('python.distutils')
pyb.use_plugin('python.pycharm')

pyb.use_plugin("filter_resources")
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
    project.get_property('coverage_exceptions').append('cli')

    project.set_property('distutils_console_scripts', ['gitpage = gitpage.cli:cli'])

    project.get_property("filter_resources_glob").append("**/gitpage/__init__.py")

    project.get_property('copy_resources_glob').append(
        'src/main/python/gitpage/templates/*')
    project.set_property('copy_resources_target', '$dir_dist')

    for template in os.listdir(os.path.join('src/main/python/gitpage/templates/')):
        project.install_file('lib/python2.7/site-packages/gitpage/templates',
                             'gitpage/templates/{0}'.format(template))


@pyb.task(description='Downloads and installs the libgit2 library before pygit2 is '
                      'installed since libgit2 is a dependency.')
@pyb.before('install_pygit2')
def install_libgit2(project, logger):
    """
    Download and install libgit2 which is required for pygit2 to successfully install.
    """
    logger.info('Installing libgit2')
    run(project, logger, 'install_libgit2',
        """cd {0}
        export LIBGIT2=$VIRTUAL_ENV
        wget https://github.com/libgit2/libgit2/archive/v0.27.0.tar.gz
        tar xzf v0.27.0.tar.gz
        cd libgit2-0.27.0/
        cmake . -DCMAKE_INSTALL_PREFIX=$LIBGIT2
        make
        make install
        """.format(project.expand('$dir_dist/dist')))


@pyb.task(description='Install pygit2 manually due to being installed into a virtual '
                      'environment.')
@pyb.depends('install_libgit2')
@pyb.before('install_dependencies')
def install_pygit2(project, logger):
    """
    Install the pygit2 library using pip and setting installation environment variables.
    """
    logger.info('Installing pygit2')
    run(project, logger, 'install_pygit2',
        """export LDFLAGS="-Wl,-rpath='$LIBGIT2/lib',--enable-new-dtags $LDFLAGS"
        pip install pygit2
        """)
    pass


@pyb.task()
@pyb.depends('install_pygit2')
def install_dependencies():
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
