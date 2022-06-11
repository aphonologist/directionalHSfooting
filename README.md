# FRedty

This repository contains a typology calculator for Harmonic Serialism based on the Fusional Reduction algorithm (FRed) (Brasoveanu & Prince 2011). The component programs are:

*    con.py defines constraints as Classes which can be evaluated traditionally or directionally
*    fred.py provides a implementation of FRed
*    gen.py defines the candidate generation function, mapping syllables (s) onto trochees (Tt), iambs (iI), and monosyllabic feet (F)
*    tabIO.py provides a pretty print function for tableaux
*    typologizer.py is the main module

To use this software, provide URs and CON to typologizer.py and run the script with Python 3. The script conducts a breadth-first search over derivations, pruning branches with unsatisfiable ranking conditions. After this search concludes, the script tests whether the directionalities of any constraints matter.

![](anifred.gif)
# directionalHSautosegments
