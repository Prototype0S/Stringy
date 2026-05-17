from ._anvil_designer import ChatComponentTemplate
from anvil import *
import anvil.server
import anvil.users


class ChatComponent(ChatComponentTemplate):

  def __init__(self, channel="General", **properties):
    self.init_components(**properties)

    # current channel (STRING ONLY)
    self.current_channel = channel

    self.channel_label.text = channel

    # load initial messages
    self.load_messages()


  # -----------------------
  # CHANNEL SWITCHING (UI ONLY)
  # -----------------------

  @handle("general", "click")
  def general_click(self, **event_args):

    self.channel_label.text = "General"
    self.current_channel = "General"
    self.load_messages()


  @handle("sheet_music", "click")
  def sheet_music_click(self, **event_args):

    self.channel_label.text = "Sheet music"
    self.current_channel = "Sheet music"
    self.load_messages()


  @handle("events", "click")
  def events_click(self, **event_args):

    self.channel_label.text = "Events"
    self.current_channel = "Events"
    self.load_messages()


  # -----------------------
  # LOAD MESSAGES
  # -----------------------

  def load_messages(self):

    messages = anvil.server.call(
      "get_messages",
      self.current_channel
    )

    print("MESSAGES:", messages)

    self.repeating_panel_messages.items = messages


  # -----------------------
  # SEND MESSAGE
  # -----------------------

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