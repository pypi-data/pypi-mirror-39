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
    'version': '0.1.1',
    'description': "Manny's code snippets",
    'long_description': '# molib\nThis package contains functions that I keep re-using in different packages, so I decided to publish it in case it helps other too.\n\n# Installation\nTo install molib, use pip (or similar):\n```{.sourceCode .bash}\npip install molib\n```\n\n# Documentation\n```python\nlabel_subplots(fig, size=14)\n  ```\nAdds letter labels to all subplots in a figure.\nAdjusts figure padding and left margin to make labels fit.\n\n```python\nadd_subfig_label(ax, label, size=14)\n```\nAdds a subplot label to an axis.\n\n```python\ngen_sub_label(lower=False, paren=False)\n```\nGenerates the next letter in the alphabet as a subfig label.\nLabel can be uppercase or lowercase, with optional parentheses.\n\n```python\nsave_plot(output_filename, proj_dir=Path.cwd(), subdir=None, fig=None)\n```\nFunction for saving plots and printing message; makes plots directory.\n',
    'author': 'Manny Ochoa',
    'author_email': 'dev@manuelochoa.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
