import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.users
from datetime import datetime, timezone


@anvil.server.callable
def get_messages(channel):

  user = anvil.users.get_user()

  messages = list(
    app_tables.messages.search(
      tables.order_by("sent_at"),
      channel=channel
    )
  )

  for m in messages:

    sender = m['user']

    m['is_me'] = (
      user is not None
      and sender is not None
      and sender.get_id() == user.get_id()
    )

  return messages


@anvil.server.callable
def send_message(channel, text):

  user = anvil.users.get_user()

  if not user or not text or not text.strip():
    return

  app_tables.messages.add_row(
    channel=channel,
    user=user,
    message=text,
    sent_at=datetime.now(timezone.utc)
  )