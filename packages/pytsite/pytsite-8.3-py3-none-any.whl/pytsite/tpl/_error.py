"""PytSite Tpl Errors
"""
import jinja2 as _jinja

__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TemplateNotFound(_jinja.TemplateNotFound):
    pass
