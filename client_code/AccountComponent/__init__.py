from ._anvil_designer import AccountComponentTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class AccountComponent(AccountComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    user = anvil.users.get_user()
    self.first_name.text = user["first_name"]
    self.last_name.text = user["last_name"]

  @handle("button_edit", "click")
  def button_edit_click(self, **event_args):
    main_form = get_open_form()
    main_form.switch_component("details")



