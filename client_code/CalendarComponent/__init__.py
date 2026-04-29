from ._anvil_designer import CalendarComponentTemplate
from anvil import *
import plotly.graph_objects as go
from anvil.tables import app_tables
from datetime import datetime


class CalendarComponent(CalendarComponentTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.warning.visible = False

    self.refresh_ui()


  # -----------------------
  # MAIN LOAD FUNCTION
  # -----------------------
  def refresh_ui(self):
    self.load_chart()
    self.load_events()


  # -----------------------
  # ADD EVENT (merged AddComponent logic)
  # -----------------------
  def button_save_click(self, **event_args):
    name = self.event_name.text
    date = self.date_picker_1.date
    start_text = self.start_time.text
    end_text = self.end_time.text

    # validation
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

    # parse time safely
    start_time = self.parse_time(start_text)
    if not start_time:
      self.show_warning("Invalid start time (use HH:MM or HH:MM AM/PM)")
      return

    end_time = self.parse_time(end_text) if end_text else None

    start_dt = datetime.combine(date, start_time)
    end_dt = datetime.combine(date, end_time) if end_time else None

    # save
    app_tables.events.add_row(
      name=name,
      start=start_dt,
      end=end_dt,
      created_by=None
    )

    self.show_success("Event saved")
    self.clear_form()
    self.refresh_ui()


  # -----------------------
  # PLOTLY CHART
  # -----------------------
  def load_chart(self):
    data = {}

    for row in app_tables.events.search():
      day = row['start'].date()
      data[day] = data.get(day, 0) + 1

    fig = go.Figure(data=[
      go.Bar(
        x=list(data.keys()),
        y=list(data.values())
      )
    ])

    self.plot_timeline.figure = fig


  # -----------------------
  # HELPERS
  # -----------------------
  def parse_time(self, text):
    formats = ["%H:%M", "%I:%M %p"]

    for fmt in formats:
      try:
        return datetime.strptime(text.strip(), fmt).time()
      except:
        pass

    return None


  def clear_form(self):
    self.event_name.text = ""
    self.date_picker_1.date = None
    self.start_time.text = ""
    self.end_time.text = ""


  def show_warning(self, msg):
    self.warning.visible = True
    self.warning.text = msg
    self.warning.foreground = "#ff0000"


  def show_success(self, msg):
    self.warning.visible = True
    self.warning.text = msg
    self.warning.foreground = "#000000"