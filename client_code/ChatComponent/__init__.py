from ._anvil_designer import ChatComponentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ChatComponent(ChatComponentTemplate):
  def __init__(self, channel="General", **properties):
    self.init_components(**properties)

    self.channel_label.text = channel
    # Any code you write here will run before the form opens.
  @handle("general", "click")
  def general_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.channel_label.text = "General"

  @handle("sheet_music", "click")
  def sheet_music_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.channel_label.text = "Sheet music"
  @handle("events", "click")
  def events_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.channel_label.text = "Events"