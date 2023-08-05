Jaynes, A Utility for training ML models on AWS, GCE, SLURM, with or without docker 
====================================================================================

Todo
----

-  [x] get the initial template to work

Done
~~~~

Installation
------------

.. code-block:: bash

    pip install jaynes

Usage (**Show me the Mo-NAY!! :moneybag::money\_with\_wings:**)
---------------------------------------------------------------

Check out the example folder for projects that you can run.

To Develop
----------

.. code-block:: bash

    git clone https://github.com/episodeyang/jaynes.git
    cd jaynes
    make dev

To test, run

.. code-block:: bash

    make test

This ``make dev`` command should build the wheel and install it in your
current python environment. Take a look at the
`https://github.com/episodeyang/jaynes/blob/master/Makefile <https://github.com/episodeyang/jaynes/blob/master/Makefile>`__ for details.

**To publish**, first update the version number, then do:

.. code-block:: bash

    make publish

Acknowledgements
----------------

This code-block is inspired by @justinfu's
`doodad <https://github.com/justinjfu/doodad>`__, which is in turn built
on top of Peter Chen's script.

This code-block is written from scratch to allow a more permissible
open-source license (BSD). Go bears :bear: !!


