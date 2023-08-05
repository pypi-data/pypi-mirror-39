import os
import abc
import functools
import json
import jsonschema

class MapperDefinition(dict):
    def __init__(self, definition):
        self.normalize(definition)
        self.validate(definition)
        super().__init__(definition)

    @classmethod
    def normalize(cls, definition):
        if 'miriam_mapping' in definition:
            # key synonyms equal to a miriam namespace contained
            # in miriam_mapping will be lost (and that is ok)
            definition['key_synonyms'] = {
                                           **definition.get('key_synonyms', {}),
                                           **definition['miriam_mapping']
                                          }
        if 'key_synonyms' in definition:
            # add key synonyms to supported keys
            definition['supported_keys'] = definition['supported_keys'] + \
                                           list(definition['key_synonyms'].keys())
        definition['supported_keys'] = list(set(definition['supported_keys']))

    @classmethod
    def validate(cls, definition):
        '''
        This static method validates a BioMapMapper definition.
        It returns None on success and throws an exception otherwise.
        '''
        schema_path = os.path.join(os.path.dirname(__file__),
                                   '../../schema/mapper_definition_schema.json')
        with open(schema_path, 'r') as jsonfp:
            schema = json.load(jsonfp)
        # Validation of JSON schema
        jsonschema.validate(definition, schema)
        # Validation of JSON properties relations
        assert definition['main_key'] in definition['supported_keys'], \
               '\'main_key\' must be contained in \'supported_keys\''
        assert set(definition.get('list_valued_keys', [])) <= set(definition['supported_keys']), \
               '\'list_valued_keys\' must be a subset of \'supported_keys\''
        assert set(definition.get('disjoint', [])) <= set(definition.get('list_valued_keys', [])), \
               '\'disjoint\' must be a subset of \'list_valued_keys\''
        assert set(definition.get('key_synonyms', {}).values()) <= set(definition['supported_keys']), \
               '\'The values of the \'key_synonyms\' mapping must be in \'supported_keys\''

    @classmethod
    def validate_data(cls, data):
        '''
        Validates data with respect to the data definition.
        '''
        pass

    @property
    def supported_keys(self):
        '''
        Returns a list with all keys which are supported by the mapper.
        '''
        return self['supported_keys']

    @property
    def name(self):
        '''
        Returns the name of the mapper.
        '''
        return self['name']

    @property
    def mapper_data(self):
        '''
        Returns the name of the data associated with the mapper.
        '''
        return self['mapper_data']

    @property
    def main_key(self):
        '''
        Returns the main key of the mapper.
        '''
        return self['main_key']

    @property
    def miriam_mapping(self):
        '''
        Returns a mapping from supported keys to official
        Miriam namespace ids (as a dictionary).
        '''
        return self.get('miriam_mapping', {})

    @property
    def scalar_nonunique_keys(self):
        '''
        Returns a list of supported keys whose values
        are scalar and possibly non-unique across data
        entries.
        '''
        return self.get('scalar_nonunique_keys', [])

    @property
    def compound_valued_keys(self):
        '''
        Returns a list of supported keys whose values are
        from some kind of (usually more complex) data structure
        (a nested dictionary for example), ie whose values
        are not strings for arrays of strings. Compound-valued
        keys can not be used to map FROM.
        '''
        return self.get('compound_valued_keys', [])

    @property
    def key_synonyms(self):
        '''
        Returns a list of key synonyms (as a dictionary).
        '''
        return self.get('key_synonyms', {})

    @property
    def disjoint(self):
        '''
        Returns all list-values keys for which it is assured
        that for any two values of that key the set of the
        entries of that value are disjoint (do not have an
        element in common).
        '''
        return self.get('disjoint', [])

    @property
    def list_valued_keys(self):
        '''
        Returns a list of supported keys whose values are
        list of strings.
        '''
        return self.get('list_valued_keys', [])


class Mapper(abc.ABC):

    def __init__(self, name, biomap_db):
        self._name = name
        self.db = biomap_db
        self._definition = self.db.get_mapper_definition(self.name)

    @property
    def name(self):
        '''
        Returns the name of the mapper.
        '''
        return self._name

    @property
    def definition(self):
        '''
        Returns the definition of the mapper.
        '''
        return self._definition

    @property
    def data(self):
        '''
        Return the entirety of the data as a list.
        '''
        return self.db.get_mapper_data(self.name)

    @property
    def miriam_namespaces(self):
        '''
        Returns a list of the supported MIRIAM namespaces.
        '''
        return [namespace for namespace in self.definition.miriam_mapping]

    def __call__(self, ID_s, FROM=None, TO=None):
        '''
        A simpler interface to Mapper.map which makes the mapper callable.
        '''
        return self.map(ID_s, FROM, TO)

    def map(self, ID_s,
                  FROM=None,
                  TO=None,
                  target_as_set=False,
                  no_match_sub=None):
        '''
        The main method of this class and the essence of the package.
        It allows to "map" stuff.

        Args:

            ID_s: Nested lists with strings as leafs (plain strings also possible)
            FROM (str): Origin key for the mapping (default: main key)
            TO (str): Destination key for the mapping (default: main key)
            target_as_set (bool): Whether to summarize the output as a set (removes duplicates)
            no_match_sub: Object representing the status of an ID not being able to be matched
                          (default: None)

        Returns:

            Mapping: a mapping object capturing the result of the mapping request
        '''
        def io_mode(ID_s):
            '''
            Handles the input/output modalities of the mapping.
            '''
            unlist_return = False
            list_of_lists = False
            if isinstance(ID_s, str):
                ID_s = [ID_s]
                unlist_return = True
            elif isinstance(ID_s, list):
                if len(ID_s) > 0 and isinstance(ID_s[0], list):
                    # assuming ID_s is a list of lists of ID strings
                    list_of_lists = True
            return ID_s, unlist_return, list_of_lists

        # interpret input
        if FROM == TO:
            return ID_s
        ID_s, unlist_return, list_of_lists = io_mode(ID_s)
        # map consistent with interpretation of input
        if list_of_lists:
            mapped_ids = [self.map(ID, FROM, TO, target_as_set, no_match_sub) for ID in ID_s]
        else:
            mapped_ids = self._map(ID_s, FROM, TO, target_as_set, no_match_sub)
        # return consistent with interpretation of input
        if unlist_return:
            return mapped_ids[0]
        return Mapping(ID_s, mapped_ids)

    def _map(self, ID_s, FROM, TO, target_as_set, no_match_sub):
        # set defaults for FROM and TO argument
        if FROM is None:
            FROM = self.definition.main_key
        if TO is None:
            TO = self.definition.main_key
        FROM = self.definition.key_synonyms.get(FROM, FROM)
        TO = self.definition.key_synonyms.get(TO, TO)
        # handle mapping attempts FROM compound keys (keys where values are arbitrary JSON objects)
        if FROM in self.definition.compound_valued_keys:
            print("BioMapMapper does not support mapping FROM compound-valued keys.")
            return None
        # --- if mapping seems feasible ---
        mapping = self._map_kernel(ID_s, FROM, TO, target_as_set)
        if no_match_sub is not None:
            mapping = [no_match_sub(ID) if mappedID is None else mappedID for ID, mappedID in zip(ID_s, mapping)]
        return mapping

    def _map_kernel(self, ID_s, FROM, TO, target_as_set):
        # handle mapping attempt FROM scalar-valued keys (keys where values are scalars (strings))
        if FROM not in self.definition.list_valued_keys:
            # branch on whether mapping is FROM nonunique or unique key
            if FROM in self.definition.scalar_nonunique_keys:
                mapping = self.from_scalar_nonunique_to_any_map_impl(ID_s, FROM, TO)
            else:
                mapping = self.one_to_any_map_impl(ID_s, FROM, TO)
        # handle mapping attempt FROM list-valued keys (keys where values are lists of scalars (strings))
        else:
            # branch on whether the values of FROM are known (or assumed...) to be disjoint
            if FROM in self.definition.disjoint:
                mapping = self.disjoint_many_to_any_map_impl(ID_s, FROM, TO)
            else:
                mapping = self.many_to_any_map_impl(ID_s, FROM, TO)
        if target_as_set and TO in self.definition.list_valued_keys:
            return [set(lst) for lst in mapping]
        elif target_as_set and TO not in self.definition.list_valued_keys:
            return set(mapping)
        return mapping

    @abc.abstractmethod
    def one_to_any_map_impl(self, ID_s, FROM, TO):
        pass

    @abc.abstractmethod
    def many_to_any_map_impl(self, ID_s, FROM, TO):
        pass

    @abc.abstractmethod
    def disjoint_many_to_any_map_impl(self, ID_s, FROM, TO):
        pass

    @abc.abstractmethod
    def from_scalar_nonunique_to_any_map_impl(self, ID_s, FROM, TO):
        pass

    def get_all(self, key=None):
        '''
        Returns all data entries for a particular key. Default is the main key.

        Args:

            key (str): key whose values to return (default: main key)

        Returns:

            List of all data entries for the key
        '''
        key = self.definition.main_key if key is None else key
        key = self.definition.key_synonyms.get(key, key)
        entries = self._get_all(key)
        if key in self.definition.scalar_nonunique_keys:
            return set(entries)
        return entries

    @abc.abstractmethod
    def _get_all(self, key):
        '''
        Backend-specific implementation of Mapper.get_all.
        '''
        pass


class MapperCollection:
    def __init__(self, name, mappers, biomap_db):
        self.name = name
        self.mappers = mappers
        self.biomap_db = biomap_db
        for mapper in self.mappers:
            self.__dict__[mapper] = self.biomap_db.get_mapper(mapper)


class Mapping(list):

    def __init__(self, origin, mapped):
        super().__init__(mapped)
        self.origin = origin
        if isinstance(self.origin[0], str):
            self.hashable_origin = True
        else:
            self.hashable_origin = False

    def as_dict(self, reverse=False):
        if not self.hashable_origin: return self
        if reverse:
            return dict(zip(self, self.origin))
        return dict(zip(self.origin, self))

    def as_set(self):
        return self.flatten()

    @classmethod
    def _flatten(cls, container):
        for elmt in container:
            if isinstance(elmt, (list,set)):
                for nested_elmt in cls._flatten(elmt):
                    yield nested_elmt
            else:
                yield elmt

    def flatten(self):
        return set(self._flatten(self))
