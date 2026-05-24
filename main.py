from nicegui import ui, app
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6
from pathlib import Path
from Shape import Shape
from Spline import Spline
from Pattern import Pattern
from Point import Point
from Interface import Interface

# Create a local directory to save PDFs if it doesn't exist
# NiceGUI needs a static folder to serve local files safely to the browser
static_dir = Path("./static")
static_dir.mkdir(exist_ok=True)

# Tell NiceGUI to serve files from the '/static' folder at the URL path '/download'
app.add_static_files('/download', str(static_dir))


current_pdf_path = None
saved = False
I = Interface()




            





def generate_pdf():
    global current_pdf_path
    global saved
    if not saved:
        delete_current_pdf()
        saved = False

    raw_filename = filename_input.value.strip() or "output"
    
    # Force the PDF to be saved inside our static directory
    pdf_path = static_dir / Path(raw_filename).with_suffix(".pdf")
    
    if not I.patterns_list and not I.splines_list:
        ui.notify("Please add at least one pattern or spline.", type='warning')
        return

    try:
        page = Pattern(filename=str(pdf_path), 
                        circles=int(circles.value),
                        lines=int(lines.value),
                        sketch=int(sketch.value),
                        cord=int(cord.value))
        shape = Shape(page, center_radius=int(radius.value))
        spline = Spline(page)
        center_points = shape.calc_shape(page.center, num_points=int(num_center_points.value))
        for cp in center_points:
            page.center = cp
            for p in I.patterns_list:
                shape.generate_shape(
                    num_shapes=int(p['num_shapes'].value),
                    size=int(p['size'].value),
                    shape=int(p['shape'].value),
                    col=p['hex'],
                    offset=float(p['offset'].value),
                    line_points=int(p['line_points'].value))
            for s in I.splines_list:
                spline.generate_spline(
                    spline=int(s['spline'].value),
                    num_points=int(s['num_points'].value),
                    start_point=(Point.from_polar(int(s['start_point'][0].value), int(s['start_point'][1].value))),
                    control_point=(Point.from_polar(int(s['control_point'][0].value), int(s['control_point'][1].value))),
                    end_point=(Point.from_polar(int(s['end_point'][0].value), int(s['end_point'][1].value))))
                
        page.savePDF()
        
        ui.notify(f"Generated {pdf_path.name}!", type='positive')
        current_pdf_path = pdf_path
        
        # --- Update the PDF Viewer Section ---
        # We point the iframe source to the local route we mapped earlier + a timestamp to force refresh
        pdf_viewer.set_visibility(True)
        pdf_frame.props(f'src="/download/{pdf_path.name}?t={time.time()}"')
    
    except Exception as e:
        ui.notify(f"Error: {str(e)}", type='negative')

def delete_current_pdf():
    global current_pdf_path
    if current_pdf_path and current_pdf_path.exists():
        try:
            # 1. Clear iframe source so the browser releases the file lock
            pdf_frame.props('src=""')
            
            # 2. Delete file from local storage
            current_pdf_path.unlink()
            ui.notify(f"Deleted {current_pdf_path.name} successfully.", type='positive')
            
            # 3. Clean up UI state
            current_pdf_path = None
            pdf_viewer.set_visibility(False)
        except Exception as e:
            ui.notify(f"Could not delete file: {str(e)}", type='negative')
    else:
        ui.notify("No generated file found to delete.", type='warning')

def save_current_pdf():
    global current_pdf_path
    global saved
    ui.notify(f"Saved {current_pdf_path.name} successfully.", type='positive')
    pdf_viewer.set_visibility(False)
    filename_input.value = ""

    current_pdf_path = None
    saved = True
    



# --- UI Layout ---
ui.query('body').classes('bg-slate-100')

# Main layout split into a 2-column grid (Left: Controls, Right: PDF Viewer)
with ui.grid(columns='1fr 1fr').classes('w-full max-w-6xl mx-auto my-10 gap-6 p-4'):
    
    # LEFT COLUMN: Controls Card
    with ui.card().classes('p-6 shadow-lg rounded-xl bg-white h-fit'):
        ui.label('PDF Pattern Generator').classes('text-2xl font-bold text-slate-800 mb-2')
        
        filename_input = ui.input(label='Filename', placeholder='output', suffix='.pdf').classes('w-full mb-4')
        cord = ui.switch('Coordinates', value=False)
        
        ui.separator().classes('my-2')
        with ui.row().classes('w-full justify-between items-center mb-2'):
            ui.label('Center').classes('text-lg font-semibold text-slate-700')
            num_center_points = ui.number(label='Points', value=1, min=1, step=1).classes('w-24')
            radius = ui.slider(min=0, max=100, step=1, value=1).classes('w-32 intermediate-class')
            ui.label().bind_text_from(radius, 'value').classes('w-12 text-right')
        ui.separator().classes('my-2')

        
        with ui.row().classes('w-full justify-between items-center mb-2'):
            ui.label('Patterns').classes('text-lg font-semibold text-slate-700')
            circles = ui.switch('Points', value=True)
            lines = ui.switch('Lines', value=True)
            sketch = ui.switch('Sketch', value=False)
        ui.separator().classes('my-2')
        with ui.row().classes('w-full items-left mb-2'):
            ui.button('Add Shape', icon='add', on_click=I.add_pattern_row).props('outline size=sm color=primary')
            ui.button('Add Spline', icon='add', on_click=I.add_spline_row).props('outline size=sm color=primary')


        patterns_container = ui.column().classes('w-full gap-3 mb-6')
        with patterns_container:
            I.add_spline_row() # Initial default row
            
        ui.button('Generate & View PDF', icon='picture_as_pdf', on_click=generate_pdf).classes('w-full py-2 text-lg').props('color=primary')

    # RIGHT COLUMN: Dynamic PDF Viewer Card
    # It starts hidden and reveals itself the first time you click "Generate"
    with ui.card().classes('p-4 shadow-lg rounded-xl bg-white h-[860px]') as pdf_viewer:
        pdf_viewer.set_visibility(False) 
        ui.label('PDF Preview').classes('text-lg font-bold text-slate-700 mb-2')
        with ui.row():
            ui.button('Delete PDF', icon='delete_forever', on_click=delete_current_pdf).props('flat color=red size=md')
            ui.button('Save PDF', icon='save', on_click=save_current_pdf).props('flat color=green size=md')

        
        # Native HTML iframe configured to fill the card space completely
        pdf_frame = ui.element('iframe').classes('w-full h-full border-none rounded-lg')

# Start NiceGUI
ui.run(title="Pattern Generator & Viewer")