# -*- coding: utf-8 -*-
'''
Contains models that deal with collections.
'''

from augeias.uri import DefaultUriGenerator


class Collection(object):
    '''
    A collection is a set of containers that can have separate logic and 
    configuration applied to it.

    Currently a collection allows making two chief distinctions:
        * Where data whilebe stored, by setting the `object_store`
        * How URI's for the collection and it's contents will be generated by
          setting a `uri_generator`
    '''

    def __init__(self, name, object_store, **kwargs):
        self.object_store = object_store
        self.name = name
        if 'uri_generator' in kwargs:
            self.uri_generator = kwargs.get('uri_generator')
        else:
            self.uri_generator = DefaultUriGenerator()
