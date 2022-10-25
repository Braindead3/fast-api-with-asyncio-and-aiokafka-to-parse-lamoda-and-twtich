from typing import TypeVar, Generic, List

from pydantic import BaseModel

SchemaType = TypeVar("SchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[SchemaType, UpdateSchemaType]):

    def __init__(self, mongo_client):
        self._collection = mongo_client.mongodb[self.Meta.collection]

    def get_all(self) -> List[SchemaType]:
        return list(self._collection.find({}, {'_id': 0}))

    def get(self, criteria: dict) -> SchemaType:
        return self._collection.find_one(criteria)

    def delete(self, criteria: dict) -> {}:
        self._collection.delete_one(criteria)
        return {'Message': 'success'}

    def delete_all(self) -> {}:
        self._collection.delete_many({})
        return {'Message': 'success'}

    def get_page(self, limit, skip) -> List[SchemaType]:
        return list(self._collection.find({}, {'_id': 0}).skip(skip).limit(limit))

    def create(self, obj: SchemaType) -> SchemaType:
        new_obj = obj.dict()
        new_obj['_id'] = obj.id
        self._collection.insert_one(new_obj)
        return self.get({'_id': obj.id})

    def update(self, obj: UpdateSchemaType) -> SchemaType:
        query = {
            '$set': {}
        }
        updated_obj = obj.dict()

        for key in updated_obj:
            if updated_obj[key] is not None:
                query['$set'][key] = updated_obj[key]

        self._collection.update_one({'_id': obj.id}, query)

        return self._collection.find_one({'_id': obj.id})

    class Meta:
        collection: str
