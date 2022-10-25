from src.domain.models.product import Product, UpdateProduct
from src.infrastructure.base_repositroy import BaseRepository


class ProductRepository(BaseRepository[Product, UpdateProduct]):
    class Meta:
        collection = 'products'
