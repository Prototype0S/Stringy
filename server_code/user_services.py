import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timezone
import anvil.server


@anvil.server.callable
def update_user(first_name, last_name):
  user = anvil.users.get_user()

  user["first_name"] = first_name
  user["last_name"] = last_name
  
@anvil.server.callable
def update_activity():
  user = anvil.users.get_user()

  if user:
    user['last_seen'] = datetime.now(timezone.utc)