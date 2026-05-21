from ._anvil_designer import ItemTemplate3Template
from anvil import *


class ItemTemplate3(ItemTemplate3Template):

  def __init__(self, **properties):

    self.init_components(**properties)

    self.label_username.text = (
      f"{self.item['first_name']} {self.item['last_name']}"
    )