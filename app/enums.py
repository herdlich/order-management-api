from enum import Enum


class ProductStatus(str, Enum):
    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    ARCHIVED = "archived"