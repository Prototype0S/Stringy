from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.server
import anvil.users

from ..HomeComponent import HomeComponent
from ..AccountComponent import AccountComponent
from ..AddComponent import AddComponent
from ..CalendarComponent import CalendarComponent
from ..SetDetailsComponent import SetDetailsComponent
from ..WelcomeComponent import WelcomeComponent
from ..FileComponent import FileComponent
from ..SetDetailsComponent import SetDetailsComponent
from ..ChatComponent import ChatComponent

class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Store the base breadcrumb text
    self.breadcrumb_stem = self.label_title.text

    # Load the initial view
    self.switch_component("home")

  # ------------------------------
  # CENTRAL NAVIGATION ROUTER
  # ------------------------------
  def switch_component(self, state, channel="General"):
    """Route to a component based on state name."""


    # Determine component + breadcrumb
    if state == "home":
      cmpt = HomeComponent()
      breadcrumb = self.breadcrumb_stem

    elif state == "calendar":
      cmpt = CalendarComponent()
      breadcrumb = self.breadcrumb_stem + " - Calendar"
      
    elif state == "chat":
      cmpt = ChatComponent(channel=channel)
      breadcrumb = self.breadcrumb_stem + " - Chat"

    elif state == "files":
      cmpt = FileComponent()
      breadcrumb = self.breadcrumb_stem + " - File Manager"

    elif state == "account":
      cmpt = AccountComponent()
      breadcrumb = self.breadcrumb_stem + " - Account"

    elif state == "details":
      cmpt = SetDetailsComponent()
      breadcrumb = self.breadcrumb_stem + " - Account - Set Details"

    
    
    else:
      # fallback
      cmpt = HomeComponent()
      breadcrumb = self.breadcrumb_stem

    # Render component
    self.content_panel.clear()
    self.content_panel.add_component(cmpt)

    # Update UI
    self.label_title.text = breadcrumb
    self.set_active_link(state)
    self.update_auth_visibility()

  # ------------------------------
  # LINK HIGHLIGHTING
  # ------------------------------
  def set_active_link(self, state):
    """Highlight the selected navigation link."""

    self.home_link.role = "selected" if state == "home" else None
    self.events_link.role = "selected" if state == "calendar" else None
    self.files_link.role = "selected" if state == "files" else None
    self.account_link.role = "selected" if state == "account" else None
    self.chat_link.role = "selected" if state == "chat" else None

  # ------------------------------
  # LOGIN/LOGOUT VISIBILITY
  # ------------------------------
  def update_auth_visibility(self):
    """Show/hide login/register/account/logout links."""
    user = anvil.users.get_user()

    self.register_link.visible = not user
    self.login_link.visible = not user
    self.account_link.visible = user
    self.logout_link.visible = user

  # ------------------------------
  # LINK HANDLERS
  # ------------------------------
  @handle("home_link", "click")
  def home_link_click(self, **event_args):
    self.switch_component("home")

  @handle("events_link", "click")
  def events_link_click(self, **event_args):
    self.switch_component("calendar")

  @handle("files_link", "click")
  def files_link_click(self, **event_args):
    self.switch_component("files")

  @handle("account_link", "click")
  def account_link_click(self, **event_args):
    self.switch_component("account")

  @handle("register_link", "click")
  def register_link_click(self, **event_args):
    anvil.users.signup_with_form(allow_cancel=True)
    self.content_panel.clear()
    self.content_panel.add_component(SetDetailsComponent())
    self.switch_component("details")

  @handle("login_link", "click")
  def login_link_click(self, **event_args):
    anvil.users.login_with_form(allow_cancel=True)
    self.switch_component("home")

  @handle("logout_link", "click")
  def logout_link_click(self, **event_args):
    anvil.users.logout()
    self.switch_component("home")

  @handle("chat_link", "click")
  def chat_link_click(self, **event_args):
    self.switch_component("chat")

  @handle("general", "click")
  def general_click(self, **event_args):
    self.switch_component("chat", "General")
  
  @handle("sheet_music", "click")
  def sheet_music_click(self, **event_args):
    self.switch_component("chat", "Sheet music")
  
  @handle("events", "click")
  def events_click(self, **event_args):
    self.switch_component("chat", "Events")
  
    
