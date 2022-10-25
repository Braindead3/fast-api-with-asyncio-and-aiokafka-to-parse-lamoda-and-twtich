import asyncio

import aiohttp
from bs4 import BeautifulSoup

from main import db_client
from src.application.product_service import ProductService
from src.domain.models.product import Product
from src.infrastructure.product_mongo_repositry import ProductRepository


class LamodaParser:
    def __init__(self):
        self.lamoda_base_url = 'https://www.lamoda.by/'

    async def get_page_content(self, url: str, session: aiohttp.ClientSession) -> list[Product]:
        async with session.get(url) as response:
            page = await response.text()

            soup = BeautifulSoup(page, 'lxml')

            return self._parse_all_products(soup)

    def _parse_all_products(self, page) -> list[Product]:
        products = []
        for product_card in page.find_all('div', class_='x-product-card__card'):
            shoe = self._parse_product_card(product_card)
            products.append(shoe)
        return products

    def _parse_product_card(self, product_card) -> Product:
        try:
            product_href = self.lamoda_base_url + product_card.a['href']
        except AttributeError:
            product_href = None
        try:
            product_price = product_card.find('span', class_='x-product-card-description__price-single').text
        except AttributeError:
            try:
                product_price = product_card.find('span', class_='x-product-card-description__price-new').text
            except AttributeError:
                product_price = None
        try:
            product_brand_name = product_card.find('div', class_='x-product-card-description__brand-name').text
        except AttributeError:
            product_brand_name = None
        try:
            product_name = product_card.find('div', class_='x-product-card-description__product-name').text
        except AttributeError:
            product_name = None

        return Product(href=product_href, name=product_name, price=product_price, brand=product_brand_name)

    @staticmethod
    async def parse_products() -> None:
        max_shoes_page = 5
        max_jacket_page = 5
        products_service = ProductService(ProductRepository(db_client))
        async with aiohttp.ClientSession() as session:
            p_id = 0
            products = []
            tasks = []
            parser = LamodaParser()

            for page in range(1, max_shoes_page + 1):
                shoes_url = f'https://www.lamoda.by/c/23/shoes-botinki/?zbs_content=js_w_icons_877999_by_1907_w_icons&page={page}'
                tasks.append(asyncio.create_task(parser.get_page_content(shoes_url, session)))

            shoes = await asyncio.gather(*tasks)

            for shoe in shoes:
                products.append(shoe)

            for page in range(1, max_jacket_page + 1):
                jacket_url = f'https://www.lamoda.by/c/357/clothes-verkhnyaya-odezhda/?sitelink=topmenuW&l=4&page={page}'
                tasks.append(asyncio.create_task(parser.get_page_content(jacket_url, session)))

            jackets = await asyncio.gather(*tasks)

            for jacket in jackets:
                products.append(jacket)

            for page_products in products:
                for product in page_products:
                    product.id = p_id
                    products_service.create_product(product)
                    p_id += 1
