Bloody Terminal
===============

A simple piece of code to help structure your console outputs. BT makes
use of colorama to provide a few options to create a consistent console
output “theme”. 

|


----

.. code:: python

    from bloodyterminal import btext

    btext.success("your string")
    btext.info("your string")
    btext.warning("your string")
    btext.error("your string")
    btext.debug("your string")
    btext.custom("your prefix", "your string")

Will result in something like this: 

|alt text|

.. |alt text| image:: https://i.imgur.com/K63a1Iy.png


|


To test this you can also use btext.demo() to get these outputs.

NOTE: There seems to be a problem with the pycharm debugger not displaying the colors. You'd have to use the terminal.

NOTE: I did not create the coloring functionality! Credit for that goes to `colorama <https://pypi.python.org/pypi/colorama>`_