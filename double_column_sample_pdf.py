from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont

font_path = "./NanumGothic_Regular.ttf"
font_name = "nanum"
pdfmetrics.registerFont(TTFont(font_name, font_path))

# Create a new PDF with 'letter' as the page size
c = canvas.Canvas("double_column.pdf", pagesize=letter)
c.setFont(font_name, 16)

# Insert the image at the top
image_path = "Choonsik.jpg"
# Sample text
left_paragraph = """
Left Paragraph: 집가고 싶다아ㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏ
"""
right_paragraph = """
Right Paragraph: 집가기 싫다아ㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏ
"""
bottom_paragraph = """
Bottom Paragraph: 으아ㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏ
"""

text = "Title: 집이 제일 좋아!"
text_width = c.stringWidth(text, font_name, 24)

# Calculate the center position and the starting Y position for the title
page_width, page_height = letter
center_x = (page_width - text_width) / 2

# Draw the string centered at the top of the page
title_y = page_height - 1 * inch  # 1 inch from the top
c.drawString(center_x, title_y, text)

# 1. Draw Image below the title
img = PILImage.open(image_path)
img_width, img_height = img.size

new_width = page_width - 2 * inch
new_height = (new_width / img_width) * img_height

# Adjust starting Y based on title height (approximated to 1 inch here)
start_y_img = title_y - 1 * inch - new_height
c.drawInlineImage(image_path, 1 * inch, start_y_img, width=new_width, height=new_height)

# 2. Draw Texts below the image
styles = getSampleStyleSheet()
normal_style = styles["BodyText"]
normal_style.fontName = font_name
normal_style.fontSize = 12

# Calculate the starting Y position for the paragraphs based on the image's height
start_y = start_y_img

# Draw the left paragraph below the image
left_p = Paragraph(left_paragraph, normal_style)
left_width, left_height = left_p.wrap(3 * inch, 9 * inch)
left_p.drawOn(c, 0.5 * inch, start_y - left_height)

# Draw the right paragraph next to the left paragraph
right_p = Paragraph(right_paragraph, normal_style)
right_width, right_height = right_p.wrap(3 * inch, 9 * inch)
right_p.drawOn(c, 4 * inch, start_y - right_height)

# Check which paragraph (left or right) is longer and adjust the start_y for the bottom paragraph
start_y -= max(left_height, right_height)

# Draw the bottom paragraph under the longer of the two columns
bottom_p = Paragraph(bottom_paragraph, normal_style)
width, height = bottom_p.wrap(
    page_width - 2 * inch, 9 * inch
)  # Taking the full width minus margins
bottom_p.drawOn(c, 0.5 * inch, start_y - height - 10)

c.save()

print("document_with_korean_string.pdf has been generated!")
