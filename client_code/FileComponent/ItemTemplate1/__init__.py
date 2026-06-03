from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.media
import anvil.tz
class ItemTemplate1(ItemTemplate1Template):

  def __init__(self, **properties):
    self.init_components(**properties)
    # ------------------------------
    # FILE NAME
    # ------------------------------
    self.label_file_name.text = (
      self.item['file_name'])

    time = (self.item['uploaded_at'].astimezone(anvil.tz.tzlocal()).strftime("%H:%M %d/%m/%Y"))

    self.label_upload_time.text = time

    media = self.item['media']
    if media:
      if media.content_type.startswith("image/"):
        self.image_1.source = media
        self.image_1.visible = True
      else:
        self.image_1.visible = False

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

      self.item.delete()
      items = list(self.parent.items)
      items.remove(self.item)
      self.parent.items = items
