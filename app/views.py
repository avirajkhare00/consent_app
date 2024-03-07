from django.shortcuts import render
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import json
import time
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

# Create your views here.


def index(request):
    return render(request, 'html/index.html')


@csrf_exempt
def post(request):
    if request.method == 'POST':
        timestamp = time.time()
        data = json.loads(request.body)
        with open(str(timestamp) + ".png", "wb") as fh:
            fh.write(base64.urlsafe_b64decode(data['signatureOutput'].split(',')[1]))
        pdf_content = data['name'] + ' has given consent to ' + data['consentForName'] + ' for:'
        consent = ''
        if data['touch']:
            consent += ' Touch '
        if data['holdingHands']:
            consent += ' Holding Hands '
        if data['kiss']:
            consent += ' Kiss '
        if data['sex']:
            consent += ' Sex '
        fileName = str(timestamp) + '.pdf'
        documentTitle = 'Consent'
        title = 'Consent'
        textLines = [
            pdf_content,
            consent,
        ]
        image = str(timestamp) + '.png'

        # creating a pdf object
        pdf = canvas.Canvas(fileName)

        # setting the title of the document
        pdf.setTitle(documentTitle)

        # registering a external font in python
        # pdfmetrics.registerFont(
        #     TTFont('abc', 'DroidSansMono.ttf')
        # )

        # creating the title by setting it's font
        # and putting it on the canvas
        # pdf.setFont('abc', 36)
        pdf.setFontSize(36)
        pdf.drawCentredString(300, 770, title)
        pdf.setFontSize(14)

        # creating the subtitle by setting it's font,
        # colour and putting it on the canvas
        pdf.setFillColorRGB(0, 0, 255)
        # pdf.setFont("Courier-Bold", 24)

        # drawing a line
        pdf.line(30, 710, 550, 710)

        # creating a multiline text using
        # textline and for loop
        text = pdf.beginText(40, 680)
        # text.setFont("Courier", 18)
        text.setFillColor(colors.black)
        for line in textLines:
            text.textLine(line)
        pdf.drawText(text)

        # drawing a image at the
        # specified (x.y) position
        pdf.drawImage(image, 130, 400, mask='auto')

        # saving the pdf
        pdf.save()
        return FileResponse(open(str(timestamp)+'.pdf', 'rb'),
                            filename='consent.pdf',
                            as_attachment=True,
                            content_type='application/pdf')
