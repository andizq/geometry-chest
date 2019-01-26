This repository is intended to be a collection of my geometry-related codes.

/trochoid
---------

Emulates the path traced by a point on a circle of radius Rp, which is co-rotating and moving forward with a reference disc of radius Rd.
The resulting traced curve is known as a trochoid (wiki).

`prolate' trochoid [Rp > Rd]
============================

.. code-block:: bash 
   
   $ python trochoid.py -Rd 5 -Rp 10 

Produces the following mp4:

.. raw:: html
   
   <iframe width="560" height="315" src="http://www.youtube.com/embed/6Dakd7EIgBE?rel=0" frameborder="0" allowfullscreen></iframe>
   
cycloid (or brachistocrone) [Rp = Rd]
=====================================

.. code-block:: bash 
   
   $ python trochoid.py -Rd 5 -Rp 5 

Produces the following mp4:   


`curtate' trochoid [Rp < Rd]
===================================
	
.. code-block:: bash 
   
   $ python trochoid.py -Rd 10 -Rp 5 

Produces the following mp4:


