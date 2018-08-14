
import os
import pybuilder.core as pyb


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
