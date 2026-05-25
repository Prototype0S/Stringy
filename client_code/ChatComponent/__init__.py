from ._anvil_designer import ChatComponentTemplate
from anvil import *
import anvil.server


class ChatComponent(ChatComponentTemplate):

  def __init__(self, channel="General", **properties):

    self.init_components(**properties)

    self.current_channel = channel
    self.channel_label.text = channel
    self.last_message_time = None
    self.load_messages()


  # ------------------------------
  # LOAD MESSAGES
  # ------------------------------
  def load_messages(self):

    messages = anvil.server.call_s(
      "get_messages", self.current_channel)

    self.repeating_panel_messages.items = messages

    if messages:
      self.last_message_time = (messages[-1]['sent_at'])


  # ------------------------------
  # SEND MESSAGE
  # ------------------------------
  @handle("send_button", "click")
  def send_button_click(self, **event_args):

    text = self.message_input.text

    if not text or not text.strip():
      return

    anvil.server.call_s(
      "send_message",
      self.current_channel,
      text
    )

    self.message_input.text = ""

    self.load_messages()

  @handle("timer_refresh", "tick")
  def timer_refresh_tick(self, **event_args):
    messages = anvil.server.call_s("get_messages", self.current_channel)

    if not messages:
      return
      
    latest = messages[-1]['sent_at']
    
    if latest != self.last_message_time:
      self.last_message_time = latest
      self.repeating_panel_messages.items = (messages)
    