from fpdf import FPDF
import os

pdf = FPDF()
pdf.add_page()
pdf.set_font('Helvetica', 'B', 24)
pdf.cell(200, 20, txt='NeuroAI Clinical Report', ln=True, align='C')
pdf.set_font('Helvetica', '', 10)
pdf.cell(200, 10, txt='Generated on: 2026-05-17', ln=True, align='C')
pdf.ln(10)
pdf.set_font('Helvetica', 'B', 14)
pdf.cell(200, 10, txt='Audio Analysis Details', ln=True)
pdf.set_font('Helvetica', '', 12)
pdf.cell(200, 10, txt='Filename: test.wav', ln=True)
pdf.ln(5)
pdf.set_font('Helvetica', 'B', 14)
pdf.cell(200, 10, txt='AI Diagnostic Result', ln=True)
pdf.set_font('Helvetica', 'B', 18)
pdf.cell(200, 15, txt='HEALTHY PROFILE', ln=True)
pdf.set_font('Helvetica', '', 12)
pdf.cell(200, 10, txt='Confidence Score: 20.00%', ln=True)
pdf.ln(10)

from PIL import Image
# create dummy image if not exists
img_path = 'scratch/temp_graph.png'
if not os.path.exists(img_path):
    from PIL import Image, ImageDraw
    im = Image.new('RGB', (300, 200), color='white')
    draw = ImageDraw.Draw(im)
    draw.rectangle([10, 10, 290, 190], outline='black')
    im.save(img_path)

pdf.image(img_path, x=30, w=150)
print('after image x', pdf.get_x(), 'y', pdf.get_y())
pdf.ln(20)
print('before rec x', pdf.get_x(), 'y', pdf.get_y())
print('l_margin', pdf.l_margin, 'r_margin', pdf.r_margin, 'epw', pdf.epw)
line_width = getattr(pdf, 'epw', pdf.w - pdf.l_margin - pdf.r_margin)
pdf.set_x(pdf.l_margin)
print('after set_x', pdf.get_x())
recommendations = [
    'Immediate medical consultation recommended.',
    'Clinical cognitive assessment advised.',
    'Lifestyle and neurological evaluation needed.',
    'Maintain regular monitoring.'
]
for rec in recommendations:
    print('multi_cell width', line_width, 'x', pdf.get_x())
    pdf.multi_cell(line_width, 10, txt=f'- {rec}')
    print('after line x', pdf.get_x(), 'y', pdf.get_y())

pdf.output('scratch/repro.pdf')
print('wrote repro.pdf')
