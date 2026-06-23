from dataclasses import dataclass
@dataclass
class Inventory: product_id:int; available_stock:int; reserved_stock:int=0

