from ._anvil_designer import MainFormTemplate
from anvil import *
from ..HomeComponent import HomeComponent
from ..AccountComponent import AccountComponent
from ..AddComponent import AddComponent
from ..CalendarComponent import CalendarComponent
from ..SetDetailsComponent import SetDetailsComponent
from ..WelcomeComponent import WelcomeComponent
from ..FileComponent import FileComponent
class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.breadcrumb_stem = self.label_title.text

    # Any code you write here will run before the form opens.
    self.content_panel.add_component(HomeComponent())
  def set_active_link(self, state):
    if state == "home":
      self.home_link.role = "selected"
    else:
      self.home_link.role = None
  # Link handlers
  @handle("files_link", "click")
  def files_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
  @handle("events_link", "click")
  def events_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(CalendarComponent())
    
  @handle("chat_link", "click")
  def chat_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()

  @handle("register_link", "click")
  def register_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()


  @handle("account_link", "click")
  def account_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(AccountComponent())
    self.label_title.text = self.breadcrumb_stem + "- Calendar"

  @handle("login_link", "click")
  def login_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear(

  @handle("logout_link", "click")
  def logout_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear(

  @handle("home_link", "click")
  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(HomeComponent())
    self.label_title.text = self.breadcrumb_stem + "- Calendar"
    self.set_active_link("home")