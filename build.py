
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


@pyb.task()
def install_libgit2():
    pass


def run(project, logger, name, command):
    """
    Run a command in a shell during a PyBuilder task saving the stdout and stderr to log
    files. If the command has a non-zero return code then this method raises an exception.
    """
    dir_logs = project.expand('$dir_logs')
    pybuilder.utils.mkdir(dir_logs)
    out_file = os.path.join(dir_logs, '{0}.log'.format(name))
    err_file = os.path.join(dir_logs, '{0}.err'.format(name))
    with open(out_file, 'w') as out:
        with open(err_file, 'w') as err:
            retcode = subprocess.call(command, shell=True, stdout=out, stderr=err)
            if retcode:
                logger.error("{2} failed. See {0} and {1} for details."
                             .format(out_file, err_file, name))
                raise Exception("{0} Failed".format(name))
