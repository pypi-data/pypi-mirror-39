# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 21:42:26 2018

@author: fumito
"""

import modelx as mx
from modelx import defcells
import modelx.core

m, base = mx.new_model(), mx.new_space(name='base')
base.new_space('child')

sub = m.new_space(name='sub')
#sub.new_cells('child')

#m.sub.add_bases(m.base)

# m---base--child
#   |
#   +-sub--child
#