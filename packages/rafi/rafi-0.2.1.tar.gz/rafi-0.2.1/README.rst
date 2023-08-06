Rafi
====

A tiny route dispatcher for `Google Cloud Functions`_.

.. code-block:: python

  app = rafi.App("demo_app")

  @app.route("/hello/<name>")
  def index(name):
      return f"hello {name}"

In your `Google Cloud Function`__ set **Function to execute** to `app`.

.. _Google Cloud Functions: https://cloud.google.com/functions/
__ `Google Cloud Functions`_
