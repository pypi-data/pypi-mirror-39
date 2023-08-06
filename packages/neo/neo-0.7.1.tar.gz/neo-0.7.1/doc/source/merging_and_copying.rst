==================================
Merging and copying objects in Neo
==================================

Copying and merging objects in Neo can sometimes have unexpected side effects,
due to the bi-directional relationships between objects, for example between
analog signals and the segment to which they belong.

Shallow copy
------------

Shallow copying with :func:`copy.copy()` can have unexpected side effects,
and should therefore be undertaken only with care.

For example, if we make a shallow copy of a signal object, 


Deep copy
---------

Deep copying _any_ object with :func:`copy.deepcopy()` will also deep copy all objects to which it is linked.
For example, deep copying a signal will create a deep copy of its parent segment (if any),
and therefore will also deep copy all other children of that segment. 
This ensures that deep copying produces an internally-consistent Neo object graph,
but can make deep copy an unexpectedly expensive operation; if you want to deep copy only a
single child object, you should unlink it from its parent before copying.

Merging
-------



