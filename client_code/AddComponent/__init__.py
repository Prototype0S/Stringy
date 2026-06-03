from ._anvil_designer import AddComponentTemplate
from anvil import *
from anvil.tables import app_tables
import anvil.users
from datetime import datetime


class AddComponent(AddComponentTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.warning.visible = False


  @handle("save", "click")
  def save_click(self, **event_args):
    name = self.event_name.text
    date = self.date_picker_1.date
    start_text = self.start_time.text
    end_text = self.end_time.text

    # --- VALIDATION ---
    missing = []

    if not name:
      missing.append("event name")
    if not date:
      missing.append("date")
    if not start_text:
      missing.append("start time")

    if missing:
      self.show_warning("Missing: " + ", ".join(missing))
      return

    # --- PARSE TIMES ---
    start_time = self.parse_time(start_text)
    if not start_time:
      self.show_warning("Invalid start time format (use HH:MM or HH:MM AM/PM)")
      return

    end_time = None
    if end_text:
      end_time = self.parse_time(end_text)
      if not end_time:
        self.show_warning("Invalid end time format")
        return

   
    start_dt = datetime.combine(date, start_time)
    end_dt = datetime.combine(date, end_time) if end_time else None

    # --- SAVE TO DATABASE ---
    app_tables.events.add_row(
      name=name,
      start=start_dt,
      end=end_dt,
      created_by=anvil.users.get_user()
    )

    # --- SUCCESS MESSAGE ---
    if end_dt:
      msg = f"{name}: {start_dt.strftime('%d %b %Y, %I:%M %p')} → {end_dt.strftime('%I:%M %p')} saved"
    else:
      msg = f"{name}: {start_dt.strftime('%d %b %Y, %I:%M %p')} saved"

    self.show_success(msg)
    self.reset_form()


  # --- TIME PARSER ---
  def parse_time(self, text):
    formats = ["%H:%M", "%I:%M %p"]

    for fmt in formats:
      try:
        return datetime.strptime(text.strip(), fmt).time()
      except:
        continue

    return None


  # --- WARNING DISPLAY ---
  def show_warning(self, message):
    self.warning.visible = True
    self.warning.text = message
    self.warning.foreground = "#ff0000"
    self.warning.icon = "fa:exclamation-triangle"


  # --- SUCCESS DISPLAY ---
  def show_success(self, message):
    self.warning.visible = True
    self.warning.text = message
    self.warning.foreground = "#000000"
    self.warning.icon = "fa:check"


  # --- RESET FORM ---
  def reset_form(self):
    self.event_name.text = ""
    self.date_picker_1.date = None
    self.start_time.text = ""
    self.end_time.text = ""