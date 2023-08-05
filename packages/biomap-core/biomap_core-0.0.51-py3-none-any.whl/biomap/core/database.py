import abc

import biomap.core.mapper

class BioMapDBConsistencyError(Exception):
    pass

class BioMapDB(abc.ABC):

    def get_mapper_definition(self, mapper_name):
        if not self.mapper_exists(mapper_name):
            return None
        mapper_definition = self._get_mapper_definition(mapper_name)
        return biomap.mapper.MapperDefinition(mapper_definition)

    @abc.abstractmethod
    def _get_mapper_definition(self, mapper_name):
        pass

    @abc.abstractmethod
    def mapper_exists(self, mapper_name):
        pass

    @abc.abstractmethod
    def mapper_data_exists(self, data_name):
        pass

    @property
    @abc.abstractmethod
    def mapper_data(self):
        pass

    def insert_mapper(self, mapper_inserter):
        self.create_mapper(mapper_inserter.mapper_definition(),
                           mapper_inserter.mapper_data())

    def create_mapper(self, mapper_definition, mapper_data=None):
        '''


        '''
        mapper_definition = biomap.core.mapper.MapperDefinition(mapper_definition)
        if self.mapper_exists(mapper_definition.name):
            raise BioMapDBConsistencyError("Mapper with name '{}' already exists."
                                           .format(mapper_definition.name))
        if mapper_data is None:
            self.define_mapper(mapper_definition)
        # ---
        else:
            if self.mapper_data_exists(mapper_definition.mapper_data):
                raise BioMapDBConsistencyError("Mapper data with name '{}' already exists."
                                               .format(mapper_definition.mapper_data))
            #self.validate_mapper(mapper_definition, mapper_data)
            self._create_mapper(mapper_definition, mapper_data)

    @abc.abstractmethod
    def _create_mapper(self, mapper_definition, mapper_data):
        pass

    def define_mapper(self, mapper_definition):
        data = self.get_mapper_data(mapper_definition.mapper_data)
        if data is None:
           raise BioMapDBConsistencyError("No mapper data of name '{}' exists."
                                          .format(mapper_definition.mapper_data))
        self.validate_mapper(mapper_definition, data)
        self._define_mapper(mapper_definition)

    @abc.abstractmethod
    def _define_mapper(self, mapper_definition):
        pass

    def get_mapper_data(self, data_name):
        if not self.mapper_data_exists(data_name):
            return None
        return self._get_mapper_data(data_name)

    @abc.abstractmethod
    def _get_mapper_data(self, data_name):
        pass

    @abc.abstractmethod
    def get_mapper(self, mapper_name):
        pass

    @property
    @abc.abstractmethod
    def mappers(self):
        return None

    @abc.abstractmethod
    def delete_mapper(self, mapper_name):
        pass

    def delete_mapper_data(self, data_name, cascade=True):
        pass

    @abc.abstractmethod
    def _delete_mapper_data(self, data_name, cascade):
        pass

    def purge_mapper(self, mapper_name, cascade=True):
        self._purge_mapper(self, mapper_name, cascade)

    @abc.abstractmethod
    def _purge_mapper(self, mapper_name, cascade):
        pass

    def update_mapper(self, mapper_name, mapper_data):
        mapper_definition = self.get_mapper_definition(mapper_name)
        if mapper_definition is None:
            raise BioMapDBConsistencyError("No mapper of name '{}' exists"
                                           .format(mapper_name))
        self.validate_mapper(mapper_definition, mapper_data)
        self._update_mapper(mapper_name, mapper_data)

    @abc.abstractmethod
    def _update_mapper(self, mapper_name, mapper_data):
        return None

    @abc.abstractmethod
    def get_mappers(self, data_name):
        pass
