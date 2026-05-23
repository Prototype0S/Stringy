from ._anvil_designer import ChatComponentTemplate
from anvil import *
import anvil.server


class ChatComponent(ChatComponentTemplate):

  def __init__(self, channel="General", **properties):

    self.init_components(**properties)

    self.current_channel = channel
    self.channel_label.text = channel

    self.load_messages()


  # ------------------------------
  # LOAD MESSAGES
  # ------------------------------
  def load_messages(self):

    self.repeating_panel_messages.items = (
      anvil.server.call(
        "get_messages",
        self.current_channel
      )
    )


  # ------------------------------
  # SEND MESSAGE
  # ------------------------------
  @handle("send_button", "click")
  def send_button_click(self, **event_args):

    text = self.message_input.text

    if not text or not text.strip():
      return

    anvil.server.call(
      "send_message",
      self.current_channel,
      text
    )

    self.message_input.text = ""

    self.load_messages()