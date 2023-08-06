# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['molib']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0,<4.0']

setup_kwargs = {
    'name': 'molib',
    'version': '0.2.0',
    'description': "Manny's code snippets",
    'long_description': '# molib\nThis package contains functions that I keep re-using in different packages, so I decided to publish them, in case it helps other too.\n\n# Installation\nTo install molib, use pip (or similar):\n```{.sourceCode .bash}\npip install molib\n```\n\n# Documentation\n\n## Figures\n\n### Add letter labels to all subplots in a figure.\n```python\nlabel_subplots(fig, size=14)\n```\n\n* Adjusts figure padding and left margin to make labels fit.\n* Uses ```add_subfig_label``` and ```gen_sub_label```.\n\n\n### Add a subplot label to an axis.\n```python\nadd_subfig_label(ax, label, size=14)\n```\n\n\n### Generate the next figure label.\n```python\ngen_sub_label(lower=False, paren=False)\n```\n\n* Produces the next letter in the alphabet as a subfig label.\n* Label can be uppercase or lowercase, with optional parentheses.\n\n\n### Save plots in a directory\n```python\nsave_plot(output_filename, proj_dir=Path.cwd(), subdir=None, fig=None)\n```\n\n* Function for saving plots (active plot or given figure) and printing a console message.\n* Saves as a 300dpi png file.\n* Makes plots directory if it does not\nexist.\n* Directory name is customizable.\n\n\n## Colors\n### Rescale RGB to values between 0 and 1\n```python\nrescale_colors(color_list)\n```\n\n### Tableau 10 Colors\n```python\ntableau10(index)\n```\n\n### Tableau 20 Colors\n```python\ntableau20(index)\n```\n\n### Tableau Color Blind 10\n```python\ntableau10blind(index)\n```\n',
    'author': 'Manny Ochoa',
    'author_email': 'dev@manuelochoa.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
