# -*- coding: UTF-8 -*-
# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

# Note that this module may not have a docstring because any
# global variable defined here will override the global
# namespace of lino/__init__.py who includes it with execfile.

# This module is part of the Lino test suite.
# To test only this module:
#
#   $ python setup.py test -s tests.PackagesTests

from __future__ import unicode_literals
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

install_requires = [
    # 'Sphinx',
    'django',
    'atelier', 'unipath', 'python_dateutil', 'dateparser',
    'etgen',
    'Babel', 'lxml',
    'beautifulsoup4',
    'pisa',
    'jinja2', 'pytidylib', 'PyYAML',
    'clint',  # lino.modlib.checkdata.management.commands
    'django-localflavor',  # lino.modlib.sepa
    # 'django-iban',  # lino.modlib.sepa
    'openpyxl', 'html2text',
    # 'cairocffi',  # 'cairocffi<0.7',
    # 'bleach',
    # 'html5lib',  # version 7x9 (not 9x9) required by bleach
    'schedule',
    'django-wkhtmltopdf',
    'beautifulsoup4']

if PY2:
    install_requires.append('reportlab<2.7')
    # install_requires.append('django<2')
    install_requires.append('weasyprint<0.43')
else:
    # install_requires.append('django')
    install_requires.append('reportlab')
    install_requires.append('weasyprint')

SETUP_INFO = dict(
    name='lino',
    version='18.11.0',
    install_requires=install_requires,
    description="A framework for writing desktop-like web applications "
                "using Django and ExtJS",
    license='BSD License',
    # obsoletes=['djangosite', 'north'],
    author='Luc Saffre',
    author_email='luc@lino-framework.org',
    url="http://www.lino-framework.org",
    # ~ test_suite = 'lino.test_apps',
    test_suite='tests')

SETUP_INFO.update(long_description="""

.. raw:: html

    <a class="reference external" 
    href="http://lino.readthedocs.io/en/latest/?badge=latest"><img
    alt="Documentation Status"
    src="https://readthedocs.org/projects/lino/badge/?version=latest"
    /></a> <a class="reference external"
    href="https://coveralls.io/github/lino-framework/book?branch=master"><img
    alt="coverage"
    src="https://coveralls.io/repos/github/lino-framework/book/badge.svg?branch=master"
    /></a> <a class="reference external"
    href="https://travis-ci.org/lino-framework/book?branch=stable"><img
    alt="build"
    src="https://travis-ci.org/lino-framework/book.svg?branch=stable"
    /></a> <a class="reference external"
    href="https://pypi.python.org/pypi/lino/"><img alt="pypi_v"
    src="https://img.shields.io/pypi/v/lino.svg" /></a> <a
    class="reference external"
    href="https://pypi.python.org/pypi/lino/"><img alt="pypi_license"
    src="https://img.shields.io/pypi/l/lino.svg" /></a>

Lino is a high-level framework for writing desktop-like customized
database applications based on `Django <https://www.djangoproject.com/>`_
and `Sencha ExtJS <http://www.sencha.com/products/extjs/>`_.
Lino applications are Django projects
where the application developer does not need to write any
URLconf, HTML nor CSS (`more <http://lino-framework.org/about/what.html>`__).
Examples of Lino applications are
`Lino Welfare <http://welfare.lino-framework.org>`__,
`Lino Così <http://cosi.lino-framework.org>`__
or
`Lino Voga <http://voga.lino-framework.org>`__
(`more <http://lino-framework.org/about/projects.html>`__)

The central project homepage is http://www.lino-framework.org

""")

SETUP_INFO.update(classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Development Status :: 5 - Production/Stable
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
Natural Language :: English
Natural Language :: French
Natural Language :: German
Operating System :: OS Independent
Topic :: Database :: Front-Ends
Topic :: Office/Business
Topic :: Software Development :: Libraries :: Application Frameworks""".splitlines())

SETUP_INFO.update(packages=[str(n) for n in """
lino
lino.api
lino.core
lino.core.auth
lino.fake_migrations
lino.history
lino.mixins
lino.modlib
lino.modlib.about
lino.modlib.awesomeuploader
lino.modlib.blacklist
lino.modlib.bootstrap3
lino.modlib.changes
lino.modlib.comments
lino.modlib.comments.fixtures
lino.modlib.dashboard
lino.modlib.davlink
lino.modlib.dupable
lino.modlib.export_excel
lino.modlib.extjs
lino.modlib.forms
lino.modlib.gfks
lino.modlib.gfks.fixtures
lino.modlib.ipdict
lino.modlib.jinja
lino.modlib.importfilters
lino.modlib.languages
lino.modlib.languages.fixtures
lino.management
lino.management.commands
lino.modlib.odata
lino.modlib.office
lino.modlib.checkdata
lino.modlib.checkdata.fixtures
lino.modlib.checkdata.management
lino.modlib.checkdata.management.commands
lino.modlib.printing
lino.modlib.restful
lino.modlib.smtpd
lino.modlib.smtpd.management
lino.modlib.smtpd.management.commands
lino.modlib.notify
lino.modlib.notify.fixtures
lino.modlib.social_auth
lino.modlib.summaries
lino.modlib.summaries.fixtures
lino.modlib.summaries.management
lino.modlib.summaries.management.commands
lino.modlib.system
lino.modlib.tinymce
lino.modlib.tinymce.fixtures
lino.modlib.uploads
lino.modlib.users
lino.modlib.users.fixtures
lino.modlib.weasyprint
lino.modlib.wkhtmltopdf
lino.projects
lino.projects.std
lino.sphinxcontrib
lino.sphinxcontrib.logo
lino.utils
lino.utils.demonames
lino.utils.mldbc
""".splitlines() if n])

SETUP_INFO.update(message_extractors={
    'lino': [
        ('**/sandbox/**', 'ignore', None),
        ('**/cache/**', 'ignore', None),
        ('**.py', 'python', None),
        ('**/linoweb.js', 'jinja2', None),
        # ~ ('**.js',                'javascript', None),
        ('**/config/**.html', 'jinja2', None),
        # ~ ('**/templates/**.txt',  'genshi', {
        # ~ 'template_class': 'genshi.template:TextTemplate'
        # ~ })
    ],
})

# SETUP_INFO.update(package_data=dict())


SETUP_INFO.update(include_package_data=True)


# def add_package_data(package, *patterns):
#     package = str(package)
#     l = SETUP_INFO['package_data'].setdefault(package, [])
#     l += [str(x) for x in patterns]
#     l.extend(patterns)
#     return l


# add_package_data('lino.modlib.davlink', '*.jnlp')
# add_package_data('lino.utils', '*.ods')
# add_package_data('lino.config', '*.html')
# add_package_data('lino.config', '*.tmpl')
# add_package_data('lino.config', 'about/*.tmpl')
# add_package_data('lino.config', 'makedocs/*.tmpl')
# add_package_data('lino.modlib.bootstrap3', 'config/bootstrap3/*.html')
# add_package_data('lino.modlib.extjs', 'config/extjs/*.html')
# add_package_data('lino.modlib.extjs', 'config/extjs/*.js')
# add_package_data('lino.modlib.languages.fixtures', '*.tab')
# add_package_data('lino.modlib.notify', 'config/notify/*.eml')

# l = add_package_data('lino.locale')
# for lng in 'de es fr et nl pt pt-br'.split():
#     l.append('lino/locale/%s/LC_MESSAGES/*.mo' % lng)
