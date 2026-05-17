import anvil.server
from anvil.tables import app_tables
import anvil.tables as tables
import anvil.users
from datetime import datetime


@anvil.server.callable
def get_messages(channel):

  return app_tables.messages.search(
    tables.order_by("sent_at"),
    channel=channel
  )


@anvil.server.callable
def send_message(channel, text):

  user = anvil.users.get_user()

  if not user:
    return

  if not text or not text.strip():
    return

  app_tables.messages.add_row(
    channel=channel,
    user=user,
    message=text,
    sent_at=datetime.now()
  )