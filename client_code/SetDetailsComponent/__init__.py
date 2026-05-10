from ._anvil_designer import SetDetailsComponentTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from ..AccountComponent import AccountComponent

class SetDetailsComponent(SetDetailsComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  @handle("button_save", "click")
  def button_save_click(self, **event_args):
    if self.text_box_first_name.text =="" and self.text_box_last_name.text =="":
      self.label_error.text = "First and last names are required"
      self.label_error.visible = True
      return
    elif self.text_box_first_name.text == "":
      self.label_error.text = "First name cannot be blank"
      self.label_error.visible = True
      return

    elif self.text_box_last_name.text == "":
      self.label_error.text = "Last name cannot be blank"
      self.label_error.visible = True
      return
    
    else:
      return
    self.label_error.visible = False
    anvil.server.call("update_user", self.text_box_first_name.text, self.text_box_last_name.text)
    main_form = get_open_form()
    main_form.content_panel.clear()
    main_form.content_panel.add_component(AccountComponent)
    main_form.label_title.text = main_form.breadcrumb_stem + " - Account"
    main_form.set_active_link(("account"))