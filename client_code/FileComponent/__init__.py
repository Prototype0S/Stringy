from ._anvil_designer import FileComponentTemplate
from anvil import *
from anvil.tables import app_tables
import anvil.tables as tables

from datetime import datetime


class FileComponent(FileComponentTemplate):

  def __init__(self, **properties):

    self.init_components(**properties)

    self.load_files()


  # ------------------------------
  # LOAD FILES
  # ------------------------------
  def load_files(self):

    rows = list(
      app_tables.files.search(
        tables.order_by(
          "uploaded_at",
          ascending=False
        )
      )
    )

    self.repeating_panel_1.items = rows
    


  # ------------------------------
  # FILE UPLOAD
  # ------------------------------
  @handle("file_loader_1", "change")
  def file_loader_1_change(self, files, **event_args):

    # single file fallback
    if not isinstance(files, list):
      files = [files]

    for file in files:

      app_tables.files.add_row(
        file_name=file.name,
        media=file,
        content_type=file.content_type,
        uploaded_at=datetime.now()
      )

    self.load_files()