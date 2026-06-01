import io
import re
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Flowable
from reportlab.lib.pagesizes import A6
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from PIL import Image as PILImage
from reportlab.platypus import Image as RLImage

class OverlayCanvas(Flowable):
    """Safely layers a Flowable Image and a Flowable Drawing using proper canvas methods."""
    def __init__(self, bg_img, fg_drawing):
        super().__init__()
        self.bg_img = bg_img
        self.fg_drawing = fg_drawing
        # Use the drawing's dimensions to tell ReportLab how much space this component takes
        self.width = fg_drawing.width
        self.height = fg_drawing.height
        
    def wrap(self, availWidth, availHeight):
        # Tells the ReportLab story layout engine the exact space required
        return self.width, self.height
        
    def draw(self):
        # 1. Draw the underlying background image safely onto the layout canvas
        self.bg_img.drawOn(self.canv, 0, 0)
        
        # 2. Layer vector lines and coordinate points over the space
        renderPDF.draw(self.fg_drawing, self.canv, 0, 0)


class PDF:
    """Implements functions to save your specific NiceGUI stitch pattern directly to an A6 PDF."""
    
    def __init__(self):
        self.display_width = A6[0]
        self.display_height = A6[1] - 0.1

    def generate_pdf(self, svg_content):
        pdf_buffer = io.BytesIO()
        
        doc = BaseDocTemplate(pdf_buffer, pagesize=A6)
        borderless_frame = Frame(
            0, 0, A6[0], A6[1],
            id='borderless_frame',
            leftPadding=0, rightPadding=0,
            topPadding=0, bottomPadding=0
        )
        template = PageTemplate(id='A6_FullPage', frames=borderless_frame)
        doc.addPageTemplates([template])
        
        styles = getSampleStyleSheet()
        story = []
            
        try:
            canvas_view_w = 300
            canvas_view_h = 425

            # Build the underlying background asset
            pillow_width = int(self.display_width)
            pillow_height = int(self.display_height)
            bg_image = PILImage.new("RGB", (pillow_width, pillow_height), "white")
            img_data = io.BytesIO()
            bg_image.save(img_data, format="PNG")
            img_data.seek(0)
            
            rl_img = RLImage(filename=img_data, width=self.display_width, height=self.display_height)
            
            # FIX FOR INVISIBLE VECTORS: 
            # Parse and swap attributes directly inside the string since svglib ignores <style>
            processed_svg = svg_content
            processed_svg = re.sub(r'stroke-width="[^"]*"', 'stroke-width="1.2"', processed_svg)
            processed_svg = re.sub(r'r="[^"]*"', 'r="2.5"', processed_svg)
            
            if 'stroke-width' not in processed_svg:
                processed_svg = processed_svg.replace('<line', '<line stroke-width="1.2"')
            if 'r="' not in processed_svg:
                processed_svg = processed_svg.replace('<circle', '<circle r="2.5"')

            # Combine everything inside a clean root namespace container without CSS blocks
            full_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" 
                                width="{self.display_width}" 
                                height="{self.display_height}" 
                                viewBox="0 0 {canvas_view_w} {canvas_view_h}">
                {processed_svg}
            </svg>'''
            
            # Stream compiled payload through svglib parser
            svg_file = io.StringIO(full_svg)
            drawing = svg2rlg(svg_file)
            
            # Match layout constraints
            drawing.width = self.display_width
            drawing.height = self.display_height
            drawing.hAlign = 'CENTER'
            
            # Stack the canvas structures 
            story.append(OverlayCanvas(rl_img, drawing))
            
        except Exception as e:
            error_msg = f"Error compiling image layers: {str(e)}"
            fallback_style = styles['Error'] if 'Error' in styles else styles['Normal']
            story.append(Paragraph(error_msg, fallback_style))
        
        doc.build(story)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()