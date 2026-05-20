from fpdf import FPDF
from datetime import datetime
from PIL import Image, ImageDraw
import os

pdf = FPDF()
pdf.add_page()
pdf.set_font('Helvetica', 'B', 24)
pdf.set_text_color(139, 92, 246)
pdf.cell(200, 20, txt='NeuroAI Clinical Report', ln=True, align='C')
pdf.set_font('Helvetica', '', 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(200, 10, txt=f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True, align='C')
pdf.ln(10)
pdf.set_font('Helvetica', 'B', 14)
pdf.set_text_color(0, 0, 0)
pdf.cell(200, 10, txt='Audio Analysis Details', ln=True)
pdf.set_font('Helvetica', '', 12)
pdf.cell(200, 10, txt='Filename: test.wav', ln=True)
pdf.ln(5)
pdf.set_font('Helvetica', 'B', 14)
pdf.cell(200, 10, txt='AI Diagnostic Result', ln=True)
pdf.set_font('Helvetica', 'B', 18)
pdf.set_text_color(46, 204, 113)
pdf.cell(200, 15, txt='HEALTHY PROFILE', ln=True)
pdf.set_font('Helvetica', '', 12)
pdf.set_text_color(0, 0, 0)
pdf.cell(200, 10, txt='Confidence Score: 20.00%', ln=True)
pdf.ln(10)

img_path = 'scratch/temp_graph.png'
if not os.path.exists(img_path):
    im = Image.new('RGB', (300, 200), 'white')
    draw = ImageDraw.Draw(im)
    draw.rectangle([10, 10, 290, 190], outline='black')
    im.save(img_path)

pdf.image(img_path, x=30, w=150)
pdf.ln(20)
pdf.set_x(pdf.l_margin)
line_width = getattr(pdf, 'epw', pdf.w - pdf.l_margin - pdf.r_margin)
print('line_width', line_width, 'x', pdf.get_x(), 'y', pdf.get_y(), 'w', pdf.w, 'l_margin', pdf.l_margin, 'r_margin', pdf.r_margin)

recommendations = [
    'Immediate medical consultation recommended.',
    'Clinical cognitive assessment advised.',
    'Lifestyle and neurological evaluation needed.',
    'Maintain regular monitoring.'
]

for rec in recommendations:
    print('rec', rec)
    pdf.set_x(pdf.l_margin)
    print('set_x', pdf.get_x())
    pdf.cell(line_width, 10, txt=f'- {rec}', ln=True)
    print('after', pdf.get_x(), pdf.get_y())

pdf.set_font('Helvetica', 'I', 9)
pdf.set_text_color(150, 150, 150)
pdf.set_x(pdf.l_margin)
line_width = getattr(pdf, 'epw', pdf.w - pdf.l_margin - pdf.r_margin)
pdf.multi_cell(
    line_width,
    5,
    txt=(
        'Medical Disclaimer: '
        'This report is AI-generated and '
        'is NOT a medical diagnosis. '
        'Consult a qualified healthcare professional.'
    )
)

output_path = 'scratch/debug_repro_route.pdf'
pdf.output(output_path)
print('PDF saved to', output_path)
