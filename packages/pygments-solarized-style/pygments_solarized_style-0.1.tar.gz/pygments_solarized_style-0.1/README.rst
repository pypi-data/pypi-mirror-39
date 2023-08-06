Install
=======

Using PyPI and pip
------------------
::

   $ pip install pygments-solarized-style


Usage Sample
------------
::

   >>> from pygments.formatter import HtmlFormatter
   >>> HtmlFormatter(style='solarizedlight').style
   <class 'pygments_solarized_style.light.LightStyle'>
   >>> HtmlFormatter(style='solarizeddark').style
   <class 'pygments_solarized_style.light.DarkStyle'>


Export the style as CSS
-----------------------
::

   pygmentize -S solarizedlight -f html > solarizedlight.css

