from ._anvil_designer import CalendarComponentTemplate
from anvil import *
import anvil.server
import anvil.users
import plotly.graph_objects as go
from datetime import datetime


class CalendarComponent(CalendarComponentTemplate):

  def __init__(self, **properties):
    self.init_components(**properties)

    self.warning.visible = False

    user = anvil.users.get_user()
    if not user:
      self.show_warning("You must be signed in")
      return

    try:
      anvil.server.call('cleanup_events')
    except:
      pass

    self.load_chart()

  # -----------------------
  # SAVE / DELETE
  # -----------------------
  def button_save_click(self, **event_args):
    user = anvil.users.get_user()
    if not user:
      self.show_warning("You must be signed in")
      return

    delete_name = (self.delete.text or "").strip()

    # DELETE MODE
    if delete_name:
      try:
        deleted = anvil.server.call('delete_event_by_name', delete_name)
        if deleted <= 0:
          self.show_warning("No matching events found")
      except:
        self.show_warning("Delete failed")

      self.delete.text = ""
      self.load_chart()
      return

    # ADD MODE
    name = (self.event_name.text or "").strip()
    date = self.date_picker_1.date
    start_text = (self.start_time.text or "").strip()
    end_text = (self.end_time.text or "").strip()

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

    start_time = self.parse_time(start_text)
    if not start_time:
      self.show_warning("Invalid start time")
      return

    end_time = self.parse_time(end_text) if end_text else None
    if end_text and not end_time:
      self.show_warning("Invalid end time")
      return

    start_dt = datetime.combine(date, start_time)
    end_dt = datetime.combine(date, end_time) if end_time else None

    try:
      anvil.server.call('add_event', name, start_dt, end_dt)
    except:
      self.show_warning("Failed to add event")
      return

    self.clear_form()
    self.load_chart()

  # -----------------------
  # CHART (Anvil-safe)
  # -----------------------
  def load_chart(self):
    rows = anvil.server.call('get_events') or []

    names = []
    starts = []
    durations = []
    hover = []

    for row in rows:
      name = getattr(row, 'name', 'Unnamed')
      start = getattr(row, 'start', None)
      end = getattr(row, 'end', None)

      if not start:
        continue

      if not end:
        end = start

      duration = (end - start).total_seconds() * 1000

      names.append(name)
      starts.append(start)
      durations.append(duration)

      hover.append(
        f"{name}<br>"
        f"{start.strftime('%H:%M')} → {end.strftime('%H:%M')}"
      )

    fig = go.Figure(
      data=[
        go.Bar(
          x=durations,
          y=names,
          base=starts,
          orientation='h',
          hovertext=hover,
          hoverinfo='text',
          text=names,
          textposition='inside',
          insidetextanchor='start'
        )
      ]
    )

    fig.update_layout(
      height=max(400, len(names) * 45),

      margin=dict(l=200, r=40, t=30, b=40),

      xaxis=dict(
        type="date",
        tickformat="%H:%M",
        title="Time"
      ),

      yaxis=dict(
        title="Events",
        automargin=True,
        autorange="reversed"
      ),

      showlegend=False
    )

    self.plot_1.figure = fig

  # -----------------------
  # HELPERS
  # -----------------------
  def parse_time(self, text):
    if not text:
      return None

    for fmt in ["%H:%M", "%I:%M %p"]:
      try:
        return datetime.strptime(text.strip(), fmt).time()
      except:
        continue

    return None

  def show_warning(self, msg):
    self.warning.visible = True
    self.warning.text = msg
    self.warning.foreground = "#ff0000"

  def clear_form(self):
    self.event_name.text = ""
    self.date_picker_1.date = None
    self.start_time.text = ""
    self.end_time.text = ""