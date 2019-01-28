This repository is intended to be a collection of my geometry-related codes.

/trochoid
---------

Emulates the path traced by a point on a circle of radius Rp, which is co-rotating and moving forward with a reference disc of radius Rd.
The resulting traced curve is known as a trochoid (`wiki <https://en.wikipedia.org/wiki/Trochoid>`_).

Generates an mp4 video using the `matplotlib.animation <https://matplotlib.org/api/animation_api.html>`_ package.

Help
====

.. code-block:: bash 
   
   $ python trochoid.py --help

   Drawing trochoids!

   optional arguments:
   	    -h, --help            show this help message and exit
  	    -Rd RD, --Rd RD       Radius of the reference disc. Defaults to 5
	    -Rp RP, --Rp RP       Radius of the circle that will trace the trochoid.
            	                  Defaults to 2*Rd
	    -o OUTPUT, --output OUTPUT
               	                  Name of the resulting mp4 video. Defaults to
                      	          'mv_trochoid.mp4'

Examples
========

prolate trochoid [Rp > Rd]
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash 
   
   $ python trochoid.py -Rd 5 -Rp 10 -o prolate.mp4 

Watch the output mp4 video `here <https://andizq.github.io/geometry-chest/trochoid/videos/#prolate>`_.
   
cycloid (or brachistocrone) [Rp = Rd]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash 
   
   $ python trochoid.py -Rd 5 -Rp 5 -o cycloid.mp4 

Watch the output mp4 video `here <https://andizq.github.io/geometry-chest/trochoid/videos/#cycloid>`_.


curtate trochoid [Rp < Rd]
^^^^^^^^^^^^^^^^^^^^^^^^^^
	
.. code-block:: bash 
   
   $ python trochoid.py -Rd 10 -Rp 5 -o curtate.mp4 

Watch the output mp4 video `here <https://andizq.github.io/geometry-chest/trochoid/videos/#curtate>`_.


