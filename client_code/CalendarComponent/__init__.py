from ._anvil_designer import CalendarComponentTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go
from datetime import datetime


class CalendarComponent(CalendarComponentTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.warning.visible = False

    # auto cleanup past events
    anvil.server.call('cleanup_events')

    self.load_chart()
    user = anvil.users.get_user()
    if user is None:
      self.show_warning("You must be signed in to use this feature")
      return
  # -----------------------
  # SAVE / DELETE LOGIC
  # -----------------------
  @handle("button_save", "click")
  def button_save_click(self, **event_args):
    user = anvil.users.get_user()
    delete_name = self.delete.text.strip() if self.delete.text else ""

    # 🧹 DELETE MODE
    if delete_name:
      deleted = anvil.server.call('delete_event_by_name', delete_name)

      if deleted <= 0:
        self.show_warning("No matching events found")

      self.delete.text = ""
      self.load_chart()
      return


    # ➕ ADD MODE
    name = self.event_name.text
    date = self.date_picker_1.date
    start_text = self.start_time.text
    end_text = self.end_time.text
    
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

    end_time = None
    if end_text:
      end_time = self.parse_time(end_text)
      if not end_time:
        self.show_warning("Invalid end time")
        return
    

    start_dt = datetime.combine(date, start_time)
    end_dt = datetime.combine(date, end_time) if end_time else None
    if user is not None:
      anvil.server.call('add_event', name, start_dt, end_dt)
      self.clear_form()
      self.load_chart()
    else:
      self.show_warning("You must be signed in to use this feature")
      self.clear_form()
      return


  # -----------------------
  # CHART (with hover fix)
  # -----------------------
def load_chart(self):
  rows = anvil.server.call('get_events')

  x = []
  y = []
  bases = []
  hovertexts = []

  for row in rows:
    start = row['start']
    end = row['end'] if row['end'] else row['start']
    name = row['name']

    duration = (end - start).total_seconds() * 1000

    x.append(duration)
    y.append(name)
    bases.append(start)

    hovertexts.append(
      f"{name}<br>"
      f"Start: {start.strftime('%H:%M')}<br>"
      f"End: {end.strftime('%H:%M')}"
    )

  fig = go.Figure()

  fig.add_trace(go.Bar(
    x=x,
    y=y,
    base=bases,
    orientation='h',

    hovertext=hovertexts,
    hoverinfo="text",

    text=y,                # puts event names on bars
    textposition="inside", # can also try "outside"
    insidetextanchor="start"
  ))

  fig.update_layout(
    height=max(400, len(y) * 45),

    margin=dict(
      l=180,   # IMPORTANT: gives room for labels
      r=40,
      t=40,
      b=40
    ),

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
    formats = ["%H:%M", "%I:%M %p"]

    for fmt in formats:
      try:
        return datetime.strptime(text.strip(), fmt).time()
      except:
        pass

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