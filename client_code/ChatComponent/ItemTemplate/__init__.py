from ._anvil_designer import ItemTemplateTemplate
from anvil import *
from datetime import timezone, timedelta

class ItemTemplate(ItemTemplateTemplate):

  def __init__(self, **properties):

    self.init_components(**properties)

    msg = self.item

    # -------------------
    # MESSAGE TEXT
    # -------------------
    self.message_text.text = msg['message']

    # -------------------
    # USER NAME
    # -------------------
    user = msg['user']

    if user:

      first = user['first_name']
      last = user['last_name']
      email = user['email']

      name = (first or "") + " " + (last or "")
      name = name.strip()

      self.username.text = name if name else email

    else:
      self.username.text = "Unknown user"


    # -------------------
    # SENT STATUS (FAST)
    # -------------------
    self.label_sent.text = (
      "✓ Sent" if msg.get('is_me') else ""
    )


    # -------------------
    # TIME
    # -------------------
    time = msg['sent_at']

    if time:
    
      australia = timezone(timedelta(hours=10))
    
      local_time = time.astimezone(australia)
    
      self.message_time.text = (
        local_time.strftime("%H:%M")
      )
    
    else:
      self.message_time.text = ""