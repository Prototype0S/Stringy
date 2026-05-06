import anvil.server
from anvil.tables import app_tables
from datetime import datetime, timezone


@anvil.server.callable
def add_event(name, start, end):
  app_tables.events.add_row(
    name=name,
    start=start,
    end=end
  )


@anvil.server.callable
def get_events():
  return list(app_tables.events.search())


@anvil.server.callable
def delete_event_by_name(name):
  name = name.strip().lower()

  rows = app_tables.events.search()

  count = 0
  for row in rows:
    if row['name'] and row['name'].strip().lower() == name:
      row.delete()
      count += 1

  return count


@anvil.server.callable
def cleanup_events():
  now = datetime.now(timezone.utc)

  for row in app_tables.events.search():
    if row['end'] and row['end'] < now:
      row.delete()