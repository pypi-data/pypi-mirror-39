#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 16:09:37 2018

@author: antony
"""

import libdna

def get_loc_from_params(id_map):
    
    if 'chr' not in id_map:
        return None
        
    if 's' not in id_map:
        return None
        
    if 'e' not in id_map:
        return None
    
    if isinstance(id_map['chr'], str):
        chr = id_map['chr']
    else:
        chr = id_map['chr'][0]
        
    if isinstance(id_map['s'], int):
        start = id_map['s']
    else:
        start = id_map['s'][0]
        
    
    if isinstance(id_map['e'], int):
        end = id_map['e']
    else:
        end = id_map['e'][0]
        
    
    if start > end:
      start = start ^ end
      end = start ^ end
      start = start ^ end
    
    return libdna.Loc(chr, start, end)
