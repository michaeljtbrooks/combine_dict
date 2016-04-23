# combine_dict
A very useful function to combine the common values in two dictionary-like objects, and also account for asymmetric keys. Preserves key order where detected.

Usage:
  from combine_dict import combine_dicts
  c = combine_dicts(a, b)

combine_dicts(a, b, op=operator.add):
    Combines the values of two dictionaries (or OrderedDicts) by using the specified operator on the values!
    Will follow the order of the first OrderedDict encountered in the args. 
    
    Usage:        
        c = combine_dicts(a, b) #Will add the values of alike keys in a and b together, then  
    
        @param a: The first dictionary, OrderedDict, or subclass thereof
        @param b: The second dictionary, OrderedDict, or subclass therof
        @keyword op: A Python operator which will be applied to matching values in both the dicts, defaults to "add"
        
        @return: A dict, or if there is a detectable order, an OrderedDict of combined values
  
