from nicegui import ui
from Dashboard import DashboardPage



@ui.page('/')
def main_page():
    page = DashboardPage()
    page.build()

ui.run(title="PDF Pattern Generator")