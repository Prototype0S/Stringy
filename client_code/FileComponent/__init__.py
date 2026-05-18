from ._anvil_designer import FileComponentTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.media


class FileComponent(FileComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("file_loader_1", "change")
  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    print(f"The file's name is: {file.name}")
    print(f"The number of bytes in the file is: {file.length}")
    print(f"The file's content type is: {file.content_type}")
    print(f"The file's contents are: '{file.get_bytes()}'")
    self.image_1.source = file

  @handle("button_download", "click")
  def button_download_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.media.download(self.image_1.source)
