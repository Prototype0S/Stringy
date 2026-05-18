from ._anvil_designer import FileComponentTemplate
from anvil import *

import anvil.media

from anvil.tables import app_tables
import anvil.tables as tables

from datetime import datetime


class FileComponent(FileComponentTemplate):

  def __init__(self, **properties):

    self.init_components(**properties)

    self.load_files()


  # ------------------------------
  # LOAD FILES INTO REPEATING PANEL
  # ------------------------------
  def load_files(self):

    rows = app_tables.files.search(
      tables.order_by(
        "uploaded_at",
        ascending=False
      )
    )

    self.repeating_panel_1.items = rows


  # ------------------------------
  # FILE UPLOAD
  # ------------------------------
  @handle("file_loader_1", "change")
  def file_loader_1_change(self, files, **event_args):

    # If only one file uploaded,
    # convert into list
    if not isinstance(files, list):
      files = [files]

    for file in files:

      app_tables.files.add_row(
        file_name=file.name,
        media=file,
        content_type=file.content_type,
        uploaded_at=datetime.now()
      )

    Notification(
      "Files uploaded successfully"
    ).show()

    self.load_files()


  # ------------------------------
  # DOWNLOAD FILE
  # ------------------------------
  @handle("button_download", "click")
  def button_download_click(self, **event_args):

    anvil.media.download(
      self.item['media']
    )


  # ------------------------------
  # DELETE FILE
  # ------------------------------
  @handle("button_delete", "click")
  def button_delete_click(self, **event_args):

    confirm_delete = confirm(
      f"Delete '{self.item['file_name']}'?"
    )

    if confirm_delete:

      self.item.delete()

      Notification(
        "File deleted"
      ).show()

      self.load_files()


  # ------------------------------
  # DISPLAY FILE NAME
  # ------------------------------
  def form_show(self, **event_args):

    if self.item:

      self.label_file_name.text = (
        self.item['file_name']
      )