.. role:: raw-html-m2r(raw)
   :format: html


:raw-html-m2r:`<p align="center">`
    :raw-html-m2r:`<img src="https://raw.githubusercontent.com/lotrekagency/cattp/master/logo.jpg" alt="Cattp Logo" />`
:raw-html-m2r:`<br>`
:raw-html-m2r:`<a href="https://travis-ci.org/lotrekagency/cattp" target="blank">
<img src="https://travis-ci.org/lotrekagency/cattp.svg?branch=master"></a>`
:raw-html-m2r:`<a href="https://codecov.io/gh/lotrekagency/cattp">
  <img src="https://codecov.io/gh/lotrekagency/cattp/branch/master/graph/badge.svg" />
</a>`


.. raw:: html

   <p>



Installation
------------

.. code-block:: sh

   pip install cattp

Usage
-----

.. code-block:: python

   from cattp.http import HttpCatResponse

   def my_view():
       return HttpCatResponse(status_code=200)

Run tests
---------

.. code-block:: sh

   $ pip install -r requirements-dev.txt
   $ make test


