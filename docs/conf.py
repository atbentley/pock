# -*- coding: utf-8 -*-
project = u'Pock'
copyright = u'2017, Andrew Bentley'
author = u'Andrew Bentley'

version = u'0.0.6'
release = u'0.0.6'

extensions = []

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
todo_include_todos = False

html_static_path = ['_static']
pygments_style = 'sphinx'
html_theme = 'alabaster'
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
    ]
}

html_theme_options = {
    'description': "Mocked Python",
    'github_user': 'atbentley',
    'github_repo': 'pock',
    'github_type': 'star',
    'github_count': False,
    'fixed_sidebar': True,
    'sidebar_collapse': True
}
