import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.users

from datetime import datetime, timezone


# =========================
# GET MESSAGES
# =========================
@anvil.server.callable
def get_messages(channel):

  user = anvil.users.get_user()

  messages = app_tables.messages.search(
    tables.order_by("sent_at"),
    channel=channel
  )

  output = []

  for m in messages:

    sender = m['user']

    is_me = (
      user is not None
      and sender is not None
      and sender.get_id() == user.get_id()
    )

    output.append({
      "id": m.get_id(),
      "message": m['message'],
      "user": sender,
      "sent_at": m['sent_at'],
      "is_me": is_me
    })

  return output


# =========================
# SEND MESSAGE
# =========================
@anvil.server.callable
def send_message(channel, text):

  user = anvil.users.get_user()

  if not user:
    return

  if not text:
    return

  text = text.strip()

  if not text:
    return

  app_tables.messages.add_row(
    channel=channel,
    user=user,
    message=text,
    sent_at=datetime.now(timezone.utc)
  )


# =========================
# DELETE MESSAGE
# =========================
@anvil.server.callable
def delete_message(message_id):

  user = anvil.users.get_user()

  if not user:
    return

  row = app_tables.messages.get_by_id(message_id)

  if not row:
    return

  # safety check so users
  # can only delete their own messages
  if row['user'] != user:
    return

  row.delete()


# =========================
# GET LATEST MESSAGE TIME
# =========================
@anvil.server.callable
def get_latest_message_time(channel):

  messages = app_tables.messages.search(
    tables.order_by("sent_at", ascending=False),
    channel=channel
  )

  latest = next(iter(messages), None)

  return latest['sent_at'] if latest else None