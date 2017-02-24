# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:08:35 2017

@author: Jorge Luis Silva C
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

#----------------------------------------------------------------------
# Nombre:       ejemplo_matplotlib_imshow.py
# PropÃ³sito:    Aprender a realizar una grÃ¡fica en 2D
#
# Origen:        Propio.
# Autor:         Luis Miguel SÃ¡nchez-Brea,JosÃ© MarÃ­a Herrera-Fernandez  
#
# CreaciÃ³n:        18 de Septiembre de 2013
# Historia:
#
# Dependencias:    numpy, matplotlib
# Licencia:        GPL
#----------------------------------------------------------------------


"""
DescripciÃ³n: En este ejemplo se muestra como realizar una grÃ¡fica en dos dimensiones 
mediante imshow
"""

import numpy as np                  # Cargamos numpy como el alias np
import matplotlib.pyplot as plt     # Crgagamos matplotlib.pyplot como el alias plt

# Creamos una figura
plt.figure()

# Creamos los arrays dimensionales
x = np.arange(-5, 5, 0.01)
y = np.arange(-5, 5, 0.01)

# Obtenemos las corrdenadas resultantes de esos arrays
X, Y = np.meshgrid(x, y)

# Definimos la grÃ¡fica sen (x^2 + y^2)
fxy = np.sin(X**2+Y**2)

# Representamos
plt.imshow(fxy);

# AÃ±adimos una colorbar
plt.colorbar();

# Mostramos en pantalla
plt.show()