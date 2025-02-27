from app.application.file_storage.product_image_storage import ProductImageFileStorage
from app.application.repositories.order_repository import OrderRepository
from app.application.repositories.product_repository import ProductRepository
from app.domain.exceptions.not_found_exception import NotFoundException


class DeleteProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepository,
        order_repository: OrderRepository,
        product_image_storage: ProductImageFileStorage,
    ):
        self.product_repository = product_repository
        self.order_repository = order_repository
        self.product_image_storage = product_image_storage

    async def execute(self, product_id: str) -> None:
        product = await self.product_repository.get_by_id(product_id)

        if product is None:
            raise NotFoundException(f"Product with id {product_id} does not exist")

        product_orders = await self.order_repository.get_by_product(product_id)

        if len(product_orders) > 0:
            for order in product_orders:
                order.product_ids.remove(product_id)

            await self.order_repository.bulk_update(product_orders)

        await self.product_image_storage.delete(product_id)

        await self.product_repository.delete(product_id)
