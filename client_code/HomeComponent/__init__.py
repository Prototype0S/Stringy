from ._anvil_designer import HomeComponentTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from datetime import datetime, timedelta

class HomeComponent(HomeComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def load_online_users(self):

    cutoff = datetime.now() - timedelta(minutes=10)

    online_users = list(
      app_tables.users.search(
        last_seen=q.greater_than(cutoff)
      )
    )

    self.repeating_panel_online.items = online_users
    @handle("timer_1", "tick")
    def timer_1_tick(self, **event_args):

      self.load_online_users()