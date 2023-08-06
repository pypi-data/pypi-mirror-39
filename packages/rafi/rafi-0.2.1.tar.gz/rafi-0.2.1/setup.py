# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['rafi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rafi',
    'version': '0.2.1',
    'description': 'A tiny route dispatcher for Google Cloud Functions.',
    'long_description': 'Rafi\n====\n\nA tiny route dispatcher for `Google Cloud Functions`_.\n\n.. code-block:: python\n\n  app = rafi.App("demo_app")\n\n  @app.route("/hello/<name>")\n  def index(name):\n      return f"hello {name}"\n\nIn your `Google Cloud Function`__ set **Function to execute** to `app`.\n\n.. _Google Cloud Functions: https://cloud.google.com/functions/\n__ `Google Cloud Functions`_\n',
    'author': 'Danilo Braband',
    'author_email': 'dbraband@gmail.com',
    'url': 'http://github.com/dabio/rafi',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
