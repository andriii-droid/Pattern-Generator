from nicegui import ui
from ui.pages.Dashboard import DashboardPage
from json_config import JSONConfig

@ui.page('/')
def main_page():
    page = DashboardPage()
    page.build()
    config = JSONConfig(page)
    config.save_config()
ui.run(title="PDF Pattern Generator")