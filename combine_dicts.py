#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Combine Dicts
	Allows the user to combine dictionary or dictionary-like objects by applying an operator to values common to both dictionaries.
	PRESERVES THE ORDER where an ordered dict is given.
	Also carries the ability to "guess" what should happen when a key exists in one dict but not the other and do the most sensible thing.
	I don't care that it looks unweildy :-)

	@author: Dr Michael J T Brooks
	@version: 20160423
	@licence: MIT (i.e. free for you to use so long as you keep this credit in your code. I am not liable for any of your losses from using this code)
"""

from __future__ import unicode_literals
from collections import OrderedDict


class NotSet(object):
    """
    Represents a NotSet item, which differs from any of the Boolean values
    """
    def __bool__(self):
        return False
    __nonzero__=__bool__
    

def combine_dicts(a, b, op=operator.add):
    """
    Combines the values of two dictionaries (or OrderedDicts) by using the specified operator on the values!
    Will follow the order of the first OrderedDict encountered in the args. 
    
    Usage:        
        c = combine_dicts(a, b) #Will add the values of alike keys in a and b together, then  
    
        @param a: The first dictionary, OrderedDict, or subclass thereof
        @param b: The second dictionary, OrderedDict, or subclass therof
	@keyword op: A Python operator which will be applied to matching values in both the dicts, defaults to "add"
        
        @return: A dict, or if there is a detectable order, an OrderedDict of combined values
    """
    outcls = dict #The class of the item we'll be returning
    if issubclass(a.__class__,OrderedDict) or issubclass(b.__class__,OrderedDict): #Order is important if an OrderedDict has been supplied 
        outcls = OrderedDict
        if issubclass(b.__class__,OrderedDict) and not issubclass(a.__class__,OrderedDict): #B is the only dict with order here, so swap em over
            first_keys = b.keys() #B keys take the order lead
            other_keys = a.keys()                    
        else:
            first_keys = a.keys()
            other_keys = b.keys()
    else:
        first_keys = a.keys() #Default where no order matters
        other_keys = b.keys()
    #Now combine into a master keylist, preserving order where possible. We cannot simply "swap" around the dicts if B is ordered, as this will bugger up subtraction / mod / division operations
    all_keys = first_keys
    for k in other_keys: #Extend the keylist with residual keys 
        if k not in all_keys:
            all_keys.append(k)
    #Now process the operation        
    out = outcls() #Our item to store the output
    for k in all_keys: #Iterate based upon A:
        try:
            a_val = a[k]
        except KeyError:
            a_val = NotSet()
        try:
            b_val = b[k]
        except KeyError: #B doesn't contain this key, thus take the A value
            b_val = NotSet()
        if isinstance(a_val,NotSet) and not isinstance(b_val, NotSet): #B is set, A isn't
            #Only b's value exists, so give a the blank value of b's class
            try:
                a_val = b_val.__class__() #Blank version of b
            except TypeError: #Happens if b is None
                if op == operator.add: #Just take B's value as adding something to nowt equals the something
                    out[k] = b_val
                else:
                    out[k] = None #We've got nothing else we can do than default to "None"
                continue 
        elif not isinstance(a_val,NotSet) and isinstance(b_val, NotSet): #A is set, B isn't
            try:
                b_val = a_val.__class__() #Blank version of A
            except TypeError: #e.g. for a custom class or a NoneType
                if op == operator.add: #Just take A's value as adding something to nowt equals the something
                    out[k] = a_val
                else:
                    out[k] = None #That's the best we can do
                continue
        #Now attempt to run the operator on the values
        try:
            comb_val =  op(a_val, b_val) #Combine as per operator
        except TypeError: #Means that this operand is not supported between the values
            comb_val = None #Default to None
        out[k] = comb_val #Store 
    return out

