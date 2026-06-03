from ._anvil_designer import HomeComponentTemplate
from anvil import *
import anvil.users
from anvil.tables import app_tables
import anvil.tables.query as q

from datetime import datetime, timedelta


class HomeComponent(HomeComponentTemplate):

  def __init__(self, **properties):

    self.init_components(**properties)

    self.load_online_users()


  def load_online_users(self):

    cutoff = (datetime.now()- timedelta(minutes=10))

    current_user = anvil.users.get_user()

    online_users = list(
      app_tables.users.search(
        last_seen=q.greater_than(cutoff)
      )
    )

    online_users = [
      user for user in online_users
      if user != current_user
    ]

    self.repeating_panel_1.items = (online_users)