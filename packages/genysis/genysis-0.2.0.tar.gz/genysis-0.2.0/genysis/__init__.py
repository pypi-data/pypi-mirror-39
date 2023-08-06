"""
GENYSIS is a generitive design toolkit for software developers.
"""
#pydoc -w genysis (build the html docs)

from .genysis import *
__version__ = '0.2.0'
__all__ = ['volumeLattice','conformalVolume','surfaceLattice','cylindricalProjection','sphericalProjection','planarProjection','boolean','convexHull','voronoi','delaunay','blend','meshSplit','meshReduce','genLatticeUnit','marchingCube','download','upload']  # visible names
