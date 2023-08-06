Unimi Unsubscribe
=============================
|pip|

Simple package to stop receiving annoying emails from Unimi.

Installation
---------------------
Just run in your terminal:

.. code:: bash

    pip install unimi_unsubscribe


How to use it
-------------------
Write a simple script like the `given example`_:

.. code:: python

    from unimi_unsubscribe import unsubscribe

    unsubscribe("name.surname@studenti.unimi.it", "my_password")

.. _given example: https://github.com/LucaCappelletti94/unimi_unsubscribe/blob/master/example.py


.. |pip| image:: https://badge.fury.io/py/unimi_unsubscribe.svg
    :target: https://badge.fury.io/py/unimi_unsubscribe


Output example
--------------------
An example of output of trhis script is the following:

.. code:: bash

    Proceeding to unsubscribe from the following lists:
    ['agevolazioni_e_convenzioni_teatro_stud@liste.unimi.it',
    'aistp-1@liste.unimi.it',
    ...
    'studenti.ultimoanno@liste.unimi.it',
    'studentiepostlaurea@liste.unimi.it']

    Remember that you can always resubscribe to these.

    Proceed? [y/n] y

    All done: you will now receive a mail from the SYMPA service with the results of the unsubscribe commands.
    Some lists cannot be unsubscribed with this channel, as they are required by the university.
    You may receive an error from those lists.