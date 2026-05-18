import anvil.pdf
import anvil.server
from anvil.tables import app_tables


@anvil.server.callable
def export_files_pdf():

  # You can render a form OR build a report
  pdf = anvil.pdf.render_form("PDFExport")

  return pdf