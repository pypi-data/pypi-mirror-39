#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:04:08 2018

@author: Antony Holmes
"""

import re

ID_STRING_REGEX = re.compile(r'^[a-zA-Z0-9\-\:\,]+$')

class Arg(object):
    def __init__(self, name, default_value=None, arg_type=None, multiple=False):
        self.__name = name
        self.__default_value = default_value
        self.__arg_type = arg_type
        self.__multiple = multiple
        
    @property
    def name(self):
        return self.__name
    
    @property
    def default_value(self):
        return self.__default_value
    
    @property
    def arg_type(self):
        return self.__arg_type
    
    @property
    def multiple(self):
        return self.__multiple
    

class ArgParser(object):
    def __init__(self):
        self.__arg_map = {}
        
    def add(self, arg, default_value=None, arg_type=None, multiple=False):
        if isinstance(arg, Arg):
            self.__arg_map[arg.name] = arg
        elif isinstance(arg, dict):
            name = next(iter(arg))
            self.__arg_map[name] = Arg(arg, default_value=arg[name], multiple=multiple)
        else:
            if arg_type is None and default_value is not None:
                arg_type = type(default_value)
                
            self.__arg_map[arg] = Arg(arg, default_value=default_value, arg_type=arg_type, multiple=multiple)
            
        return self
            
    def parse(self, request, id_map=None):
        if id_map is None:
            id_map = {}
        
        for name, arg in self.__arg_map.items():
            
            if name in request.GET:
                values = []
                
                for x in request.GET.getlist(name):
                    if arg.arg_type is int:
                        x2 = x.replace(',', '')
                        if x2.isdigit():
                            values.append(int(x2))
                    elif arg.arg_type is float:
                        x2 = x.replace(',', '')
                        if x2.replace('.', '').isdigit():
                            values.append(float(x2))
                    else:
                        values.append(x)
                
                if arg.multiple:
                    id_map[name] = values
                else:
                    if len(values) > 0:
                        id_map[name] = values[0]
            else:
                if arg.default_value is not None:
                    id_map[name] = arg.default_value
                    
        return id_map
        
    

def parse_arg(x, name, param_spec):
    """
    Parse a string argument and attempt to turn numbers into actual
    number types.
    
    Parameters
    ----------
    x : str
        A string arg.
    
    Returns
    -------
    str, float, or int
        x type converted.
    """
    
    if isinstance(param_spec, tuple):
        default_value = tuple[0]
        param_type = tuple[1]
    else:
        default_value = param_spec
        param_type = type(default_value)

    if x.replace('.', '').isdigit():
        if x.isdigit():
            x = int(x)
        else:
            x = float(x)
    
    # if the param type does not match its spec, use the default
    if (param_type == 'id' and not ID_STRING_REGEX.match(x)) or type(x) != param_type:
        x = default_value
                
    return x


def parse_params(request, params, id_map=None):
    """
    Parse ids out of the request object and convert to ints and add
    as a named list to the id_map.
    
    Parameters
    ----------
    request : request
        URL request
    *args
        List of strings of id names to parse
    **kwargs
        If a map parameter named 'id_map' is passed through kwargs,
        it will have the ids loaded into it. In this way existing
        maps can be used/reused with this method rather than creating
        a new map each time.
        
    Returns
    -------
    dict
        dictionary of named ids where each entry is a list of numerical
        ids. This is to allow for multiple parameters with the same
        name.
    """
    
    if id_map is None:
        id_map = {}
    
    for name, param_spec in params.items():
        if name in request.GET:
            # if the sample id is present, pass it along
            values = [parse_arg(x, name, param_spec) for x in request.GET.getlist(name)]
            
            if len(values) > 0:
                # Only add non empty lists to dict
                id_map[name] = values
        else:
            # If arg does not exist, supply a default
            
            if isinstance(param_spec, tuple):
                if param_spec[0] is not None:
                    id_map[name] = [param_spec[0]]
            else:
                if param_spec is not None:
                    id_map[name] = [param_spec]
            
            
    return id_map
