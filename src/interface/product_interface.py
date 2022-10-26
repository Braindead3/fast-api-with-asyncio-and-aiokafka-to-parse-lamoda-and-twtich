from typing import Optional

from fastapi import Path, Query, APIRouter
from starlette import status

from main import db_client
from src.application.parsers.lamoda_parser import LamodaParser
from src.application.product_service import ProductService
from src.domain.models.product import Product, UpdateProduct
from src.infrastructure.product_mongo_repositry import ProductRepository

router = APIRouter(prefix="/products", tags=['lamoda'])

product_service = ProductService(ProductRepository(db_client))


@router.get('/', response_model=list[Product])
async def get_all_products() -> list[Product]:
    return product_service.get_all_products()


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def del_all_products():
    return product_service.delete_all_products()


@router.get('/{product_id}', response_model=Product)
async def get_product_by_id(
        product_id: int = Path(None, description='The ID of the product you would like to view', gte=0)) -> Product:
    return product_service.get_product_by_id(product_id)


@router.get('/{product_name}', response_model=Product)
async def get_product_by_name(product_name: Optional[str] = None) -> Product:
    return product_service.get_product_by_name(product_name)


@router.post('/', response_model=Product)
async def create_product(product: Product) -> Product:
    return product_service.create_product(product)


@router.put('/', response_model=Product)
async def update_product(product: UpdateProduct) -> Product:
    return product_service.update_product(product)


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int = Path(description='The ID of the product to delete')) -> {}:
    return product_service.delete_product(product_id)


@router.get('/parse-all')
async def parse_all_products() -> None:
    parser = LamodaParser()
    await parser.parse_products()


@router.get('/get-page', response_model=list[Product])
async def get_page(skip: int = Query(..., description='How much documents do you want to skip'),
                   limit: int = Query(..., description='How much documents do you want to receive')) -> list[Product]:
    return product_service.get_page(skip, limit)
