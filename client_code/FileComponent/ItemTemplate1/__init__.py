from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)

    def __init__(self, **properties):

      self.init_components(**properties)

    self.label_file_name.text = (
      self.item['file_name']
    )


  @handle("button_download", "click")
  def button_download_click(self, **event_args):

    media = self.item['media']

    # PDF → open in browser
    if media.content_type == "application/pdf":
      anvil.media.open_media(media)

    # Images → preview or open
    elif media.content_type.startswith("image/"):
      anvil.media.open_media(media)

    # Everything else → download
    else:
      anvil.media.download(media)


  @handle("button_delete", "click")
  def button_delete_click(self, **event_args):

    if confirm(
      f"Delete '{self.item['file_name']}'?"
    ):

      self.item.delete()

      self.parent.parent.load_files()