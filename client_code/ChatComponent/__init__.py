from ._anvil_designer import ChatComponentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.js


class ChatComponent(ChatComponentTemplate):

  def __init__(self, channel="General", **properties):
    self.init_components(**properties)

    # Current channel
    self.current_channel = channel

    # Set title
    self.channel_label.text = channel

    # Load first messages
    self.load_messages()


  # =====================================
  # CHANNEL SWITCHING
  # =====================================

  @handle("general", "click")
  def general_click(self, **event_args):

    self.current_channel = "General"
    self.channel_label.text = "General"

    self.load_messages()


  @handle("sheet_music", "click")
  def sheet_music_click(self, **event_args):

    self.current_channel = "Sheet music"
    self.channel_label.text = "Sheet music"

    self.load_messages()


  @handle("events", "click")
  def events_click(self, **event_args):

    self.current_channel = "Events"
    self.channel_label.text = "Events"

    self.load_messages()


  # =====================================
  # LOAD MESSAGES
  # =====================================

  def load_messages(self):

    messages = anvil.server.call(
      "get_messages",
      self.current_channel
    )

    self.repeating_panel_messages.items = messages

    # Wait briefly so UI finishes rendering
    anvil.js.window.setTimeout(
      self.scroll_to_latest_message,
      30
    )


  # =====================================
  # AUTO SCROLL
  # =====================================

  def scroll_to_latest_message(self):

    components = self.repeating_panel_messages.get_components()

    if len(components) > 0:

      latest_message = components[-1]

      latest_message.scroll_into_view()


  # =====================================
  # SEND MESSAGE
  # =====================================

  @handle("send_button", "click")
  def send_button_click(self, **event_args):

    text = self.message_input.text

    # Prevent empty messages
    if not text or not text.strip():
      return

    # Send to server
    anvil.server.call(
      "send_message",
      self.current_channel,
      text
    )

    # Clear input box
    self.message_input.text = ""

    # Reload messages
    self.load_messages()