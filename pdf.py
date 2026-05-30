import io
import re
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A6
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.flowables import Image as RLImage
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

class OverlayCanvas(KeepTogether):
    def __init__(self, bg_img, fg_drawing):
        super().__init__([bg_img])
        self.bg_img = bg_img
        self.fg_drawing = fg_drawing
        
    def draw(self):
        # Draw pure white background surface
        self.bg_img.draw()
        # Layer vector lines and coordinate points over the space
        renderPDF.draw(self.fg_drawing, self.canv, 0, 0)


class PDF:
    """Implements functions to save your specific NiceGUI stitch pattern directly to an A6 PDF."""
    
    def __init__(self):
        # Precise A6 point size constraints for ReportLab layout placement
        self.display_width = A6[0]
        self.display_height = A6[1] - 0.1

    def generate_pdf(self, svg_content):
        pdf_buffer = io.BytesIO()
        
        # Initialize the native zero-padding document structure
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
            # 1. Setup exact bounds based on your coordinate string workspace
            # Your coordinates naturally range up to ~265 in X and ~326 in Y.
            # A 300 x 425 boundary box maps your pattern perfectly to the A6 page aspect ratio.
            canvas_view_w = 300
            canvas_view_h = 425

            # 2. Build the underlying background asset block using integers for Pillow
            pillow_width = int(self.display_width)
            pillow_height = int(self.display_height)
            bg_image = PILImage.new("RGB", (pillow_width, pillow_height), "white")
            img_data = io.BytesIO()
            bg_image.save(img_data, format="PNG")
            img_data.seek(0)
            
            rl_img = RLImage(filename=img_data, width=self.display_width, height=self.display_height)
            
            # 3. FIX FOR INVISIBLE VECTORS: 
            # We inject a CSS style block directly inside the compiler stream.
            # This boosts line weights from 0.2 to a crisp 1.2 points so they print perfectly.
            style_overrides = """
            <style>
                line {
                    stroke-width: 1.2px !important;
                }
                circle {
                    r: 2.5px !important;
                }
            </style>
            """

            # Combine everything inside a clean root namespace container
            full_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" 
                                width="{self.display_width}" 
                                height="{self.display_height}" 
                                viewBox="0 0 {canvas_view_w} {canvas_view_h}">
                {style_overrides}
                {svg_content}
            </svg>'''
            
            # 4. Stream compiled payload through svglib parser
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