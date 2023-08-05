from .combinationdict import CombinationDict as cdict

from collections.abc import Mapping
import re


def _substitute_variable(match):
    pass

def _substitute_params( marker, all_keys, v ):
    match = marker.search( v )
    seen = set()
    while match:
        sub, key = match.groups()[ 0 ], match.groups()[ 1 ]
        if key in seen:
            raise Exception( key )
        seen.add( key )
        if key in all_keys:
            v = re.sub( re.escape( sub ), str( all_keys[ key ] ).replace( '\\', r'\\' ), v )
            match = marker.search( v )
        else:
            match = None
    return v


def _identify_item( marker, all_keys, v ):
    if isinstance( v, str ):
        return _substitute_params( marker, all_keys, v )
    elif isinstance( v, list ):
        return [ _identify_item( marker, all_keys, i ) for i in v ]
    else:
        return v


def _resolve( marker, all_keys, src ):
    result = src.copy()
    for k, v in src.items():
        if isinstance( v, Mapping ):
            result[ k ] = _resolve( marker, all_keys, v )
        else:
            result[ k ] = _identify_item( marker, all_keys, v )
    return result


class Registry:
    """ A settings registry for managing multiple levels of config handler.

        Handlers are mapping objects, with the possibility of having
        variable substitution. Handlers added later in a sequence of
        additions override keys already seen.

        Variable substitution can be forward or backward looking, i.e.
        an earlier handler might reference a key in a later handler.

        The marker for variable substitution can be configured, and
        is a regex.
    """
    def __init__( self, separator='.', marker=r'(\$\{(.*?)\})' ):
        self.data = cdict( separator )
        self.marker_pattern = re.compile( marker )

    def add( self, handler ):
        """ Add a new handler to the registry
        :param handler: A Mapping object with new settings
        :return: self: this is a builder method
        """
        self.data.update( handler )
        return self

    def resolve( self ):
        """ Apply variable substitutions on all registered handlers.
        :return: A copy of the CombinationDict Mapping object with all variable substitutions applied
        """
        self.data = _resolve( self.marker_pattern, self.data, self.data )
        return self.data
