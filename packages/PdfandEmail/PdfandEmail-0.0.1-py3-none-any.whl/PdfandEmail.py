"""
This library serves two main purposes:
1. Detect the inputFile that you send as argument. If it is a document format, a md format, or an image the library will convert the input file to a pdf
2. The library also facilitates email.If the user provides username, password, senders and receivers address and a pdf file as input arguments, the pdf file is attached and is sent to the receiver's address.
"""

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib import response
import pypandoc
import img2pdf


documentExtension = [".docx", ".doc", ".rtf"]
imageExtension = [".jpeg", ".jpg", ".png"]


def convertToPdf(inputFile):
    """
    This module detects the inputFile that you send as argument.
    If it is a document format, a md format, or an image the library will convert the input file to a pdf using dfferent pdf libraries

         Takes .
            :param inputFile: The list that is to be sorted
            :return: returns true if the input is a document file, image file or an md file


    >>> convertToPdf("Proposal.docx")
    True

    >>> convertToPdf("Movie1.jpeg")
    True
    """

    if inputFile.endswith(".md"):
        pypandoc.convert_file(inputFile, 'pdf', outputfile="Markdowntopdf.pdf")
        return True

    for docex in documentExtension:
        if inputFile.endswith(docex):
            pypandoc.convert_file(inputFile, 'pdf', outputfile="Documenttopdf.pdf")
            return True

    for imagex in imageExtension:
        if inputFile.endswith(imagex):
            with open("Imagetopdf.pdf", "wb") as f:
                f.write(img2pdf.convert(inputFile))
                return True



def email(username, password, senderAddress, receiverAddress, subject, body, inputFile):
    """
    This module facilitates email.If the user provides username, password, senders and receivers address and a pdf file as input arguments, the pdf file is attached and is sent to the receiver's address.
    """
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = senderAddress
    message['To'] = receiverAddress

    body = MIMEText(body, 'html')
    message.attach(body)
    # pdfattach = convertToPdf(inputFile)
    fileToAttach = MIMEApplication(open(inputFile, "rb").read())
    fileToAttach.add_header('Content-Disposition', 'attachment', filename=inputFile)
    message.attach(fileToAttach)
    server = smtplib.SMTP('smtp.gmail.com', '587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(senderAddress, receiverAddress, message.as_string())
    server.quit()
    return True


if __name__ == "__main__":
    import doctest
    doctest.testmod()
