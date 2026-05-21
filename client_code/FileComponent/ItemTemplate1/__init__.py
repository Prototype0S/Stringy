from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.media

class ItemTemplate1(ItemTemplate1Template):

  def __init__(self, **properties):

    self.init_components(**properties)

    self.label_file_name.text = (
      self.item['file_name']
    )


  # ------------------------------
  # OPEN / DOWNLOAD FILE
  # ------------------------------
  @handle("button_download", "click")
  def button_download_click(self, **event_args):

    media = self.item['media']

    # PDFs + images open in browser
    if (
      media.content_type == "application/pdf"
      or
      media.content_type.startswith("image/")
    ):

      anvil.media.download(media)

    # everything else downloads
    else:

      download(media)


  # ------------------------------
  # DELETE FILE
  # ------------------------------
  @handle("button_delete", "click")
  def button_delete_click(self, **event_args):

    if confirm(
      f"Delete '{self.item['file_name']}'?"
    ):

      # delete from database
      self.item.delete()

      # current repeating panel items
      items = list(self.parent.items)

      # remove current item
      items.remove(self.item)

      # update repeating panel
      self.parent.items = items
