
import os
from pybuilder.core import use_plugin, init


use_plugin('python.core')
use_plugin('python.unittest')
use_plugin('python.install_dependencies')
use_plugin('python.flake8')
use_plugin('python.coverage')
use_plugin('python.distutils')
use_plugin('python.pycharm')

use_plugin("filter_resources")
use_plugin('copy_resources')

name = 'gitpage'
default_task = 'publish'


@init
def set_properties(project):
    project.build_depends_on('service')
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
