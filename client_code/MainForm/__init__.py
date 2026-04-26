from ._anvil_designer import MainFormTemplate
from anvil import *
from ..HomeComponent import HomeComponent
class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("files_link", "click")
  def files_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass  # Write Code Here

  @handle("events_link", "click")
  def events_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass  # Write Code Here

  @handle("chat_link", "click")
  def chat_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass  # Write Code Here

  @handle("register_link", "click")
  def register_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass  # Write Code Here

  @handle("account_link", "click")
  def account_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass  # Write Code Here

  @handle("login_link", "click")
  def login_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass  # Write Code Here

  @handle("logout_link", "click")
  def logout_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass  # Write Code Here

  @handle("home_link", "click")
  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(HomeComponent)
