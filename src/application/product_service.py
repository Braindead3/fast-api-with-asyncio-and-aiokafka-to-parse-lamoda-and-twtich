from fastapi import HTTPException, status

from src.domain.models.product import Product, UpdateProduct
from src.infrastructure.product_mongo_repositry import ProductRepository


class ProductService:

    def __init__(self, product_repo: ProductRepository):
        self._product_repository = product_repo

    def get_all_products(self) -> list[Product]:
        return self._product_repository.get_all()

    def get_product_by_id(self, product_id: int) -> Product:
        product = self._product_repository.get({'_id': product_id})
        if product:
            return product
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object ID is does not exists')

    def get_product_by_name(self, product_name: str) -> Product:
        product = self._product_repository.get({'name': product_name})
        if product:
            return product
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object is does not exists')

    def create_product(self, product: Product) -> Product:
        if not self._product_repository.get({'_id': product.id}):
            return self._product_repository.create(product)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Object already exists')

    def update_product(self, product: UpdateProduct) -> Product:
        if not self._product_repository.get({'_id': product.id}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object does not exists')
        return self._product_repository.update(product)

    def delete_product(self, product_id: int) -> {}:
        if not self._product_repository.get({'_id': product_id}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object does not exists')

        return self._product_repository.delete({'_id': product_id})

    def delete_all_products(self) -> {}:
        return self._product_repository.delete_all()

    def get_page(self, skip: int, limit: int):
        return self._product_repository.get_page(limit, skip)
