from biomap.core.mapper import Mapper

class MapperDoesNotExist(Exception):
    pass

class MongoDBMapper(Mapper):
    def __init__(self, mapper_name , biomap_db):
        super().__init__(mapper_name, biomap_db)
        if self.definition is None:
            raise MapperDoesNotExist
        self.data_collection = self.db.db.get_collection(self.definition['mapper_data'])

    def find(self, *query):
        return self.data_collection.find(*query)

    def find_one(self, *query):
        return self.data_collection.find_one(*query)

    def one_to_any_map_impl(self, ID_s, FROM, TO):
        # FROM values scalar
        # 1-to-1 or 1-to-n mappings
        matches = self.find( { FROM : { '$in' : ID_s } } )
        mapping = { match[FROM]: match.get(TO, None) for match in matches }
        return [ mapping.get(ID, None) for ID in ID_s ]

    def many_to_any_map_impl(self, ID_s, FROM, TO):
        # FROM values of list type
        # n-to-1 or n-to-m mappings
        def get_matches(from_scalar, matches):
            return [match.get(TO, None) for match in matches if from_scalar in match[FROM]]
        matches = self.find( { FROM : { '$in' : ID_s } } )
        matches = [match for match in matches] # get a grip on cursor
        return [get_matches(ID, matches) for ID in ID_s]

    def disjoint_many_to_any_map_impl(self, ID_s, FROM, TO):
        # FROM values of list type where all lists are (assumed to be) disjoint
        # n-to-1 or n-to-m mappings
        matches = self.find( { FROM : { '$in' : ID_s } } )
        matches = [match for match in matches] # get a grip on cursor
        mapping = { ID : match.get(TO, None) for ID in ID_s for match in matches if ID in match[FROM] }
        return [ mapping.get(ID, None) for ID in ID_s ]

    def from_scalar_nonunique_to_any_map_impl(self, ID_s, FROM, TO):
        matches = self.data_collection.find( { FROM: { '$in': ID_s } } )
        matches = [match for match in matches] # get a grip on cursor
        mapping = { ID : [match.get(TO, None) for match in matches if ID == match[FROM]] for ID in ID_s }
        return [ mapping.get(ID, None) for ID in ID_s ]

    def _get_all(self, key):
        return [entry[key] for entry in self.data_collection.find() if entry.get(key, None)]
