from ._anvil_designer import ItemTemplateTemplate
from anvil import *
from datetime import timezone, timedelta
import anvil.server

class ItemTemplate(ItemTemplateTemplate):

  def __init__(self, **properties):

    self.init_components(**properties)
    msg = self.item
    self.message_text.text = msg['message']
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

    self.label_sent.text = ("✓ Sent" if msg.get('is_me') else "")
    self.button_delete.visible = (True if msg.get('is_me') else False)

    # -------------------
    # TIME
    # -------------------
    time = msg['sent_at']

    if time:
    
      australia = timezone(timedelta(hours=10))
    
      local_time = time.astimezone(australia)
    
      self.message_time.text = (local_time.strftime("%H:%M"))
    
    else:
      self.message_time.text = ""

  @handle("button_delete", "click")
  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    #print("clicked")

    anvil.server.call_s('delete_message', self.item['id'])

    self.remove_from_parent()

