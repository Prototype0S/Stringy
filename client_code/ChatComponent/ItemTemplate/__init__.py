from ._anvil_designer import ItemTemplateTemplate
from anvil import *
from datetime import timezone, timedelta


class ItemTemplate(ItemTemplateTemplate):

  def __init__(self, **properties):
    self.init_components(**properties)

    msg = self.item

    user = msg['user']

    if user:
      first = user['first_name']
      last = user['last_name']
      email = user['email']
      print(first, last, email)

      if first or last:
        self.username.text = f"{first or ''} {last or ''}".strip()
      else:
        self.username.text = email
    else:
      self.username.text = "Unknown user"

    # -------------------
    # MESSAGE
    # -------------------
    self.message_text.text = msg['message']

    # -------------------
    # TIME (BRISBANE)
    # -------------------
    brisbane = timezone(timedelta(hours=10))
    time = msg['sent_at']

    if time:
      self.message_time.text = time.astimezone(brisbane).strftime("%H:%M")
    else:
      self.message_time.text = ""