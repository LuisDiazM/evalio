from typing import Dict, List
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
import io
from PIL import Image
import os 

TITLE = "Hoja de respuestas"
LIMIT_CARACTERS = 25
def render_page(c:canvas.Canvas, students: List[Dict]) -> canvas.Canvas:
   
    width, height = letter
    for index, student in enumerate(students):
        student_info = {
            "student_id": student.get("student_id"),
            "template_response_id": student.get("template_response_id"),
            "group_id": student.get("group_id")}
        student_name = student.get("name","")
        if len(student_name)>LIMIT_CARACTERS:
            student_name = student_name[:LIMIT_CARACTERS]
        student_id = student.get("student_id")
        subject_name = student.get("subject")

        fecha_examen = student.get("date")
        if len(subject_name)>LIMIT_CARACTERS:
            subject_name = subject_name[:LIMIT_CARACTERS]

        # x position dynamic by position
        x_reference = width / 3 - 190
        x_reference = index * width / 3 + x_reference
        
        # title 
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_reference, height - 20, TITLE)

        # QR code generation
        qr_data = str(student_info)
        qr = qrcode.make(qr_data)
        qr_buffer = io.BytesIO()
        qr.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        qr_image = Image.open(qr_buffer)
        qr_path = f"temp/{student_name}_{student_id}.png"
        qr_image.save(qr_path, format='PNG')
        c.drawImage(qr_path, x_reference - 10,
                    height - 180, width=150, height=150)

        #student data
        c.setFont("Helvetica", 12)
        text_y = height - 190
        c.drawString(x_reference, text_y, f"{student_name}")
        c.drawString(x_reference, text_y - 20,
                     f"Identificación: {student_id}")
        c.drawString(x_reference, text_y - 40, f"{subject_name}")
        c.drawString(x_reference, text_y - 60, f"Fecha examen: {fecha_examen}")

        c.drawImage("img/automatic-grader.jpg", x_reference - 30, -270)
        os.remove(qr_path)

    return c


if __name__ == "__main__":
    students = [{
        "name": "Luis Miguel Díaz Morales",
        "student_id": "43324234233444",
        "template_response_id": "fsdfasdf",
        "group_id": "fasdfasdfasdf",
        "subject": "Administración de organizaciones",
        "date": "9 abril 2025"
    },
        {
        "name": "Luis Jose Maria Cordoba Londoño uribe serrano",
        "student_id": "41234123412442",
        "template_response_id": "fsdfasdf",
        "group_id": "fasdfasdfasdf",
        "subject": "Circuitos",
        "date": "9 abril 2025"
    },
        {
        "name": "Ingri Yulieth Rojas",
        "student_id": "1423412342134",
        "template_response_id": "fsdfasdf",
        "group_id": "fasdfasdfasdf",
        "subject": "Administración de organizaciones",
        "date": "9 abril 2025"
    }]

    # Canvas reference to make pdf
    output_path = "temp/responses_sheet.pdf"
    c = canvas.Canvas(output_path, pagesize=letter)
    students_group = [tuple(students[i:i+3]) for i in range(0, len(students), 3)]
    for student_group in students_group:
        render_page(c, student_group)
        c.showPage()
    c.save()
