## Description
    This is a module that serves two purposes:
    1. This library serves two main purposes:
        Detect the inputFile that you send as argument. If it is a document format, a md format, or an image the library will convert the input file to a pdf
    2. The library also facilitates email.If the user provides username, password, senders and receivers address and a pdf file as input arguments, the pdf file is attached and is sent to the receiver's address.
    
    ## Installation
    pip install PdfandEmail


    ## Usage
     from PdfandEmail import convertToPdf, email
    
 
    ### To convert any file (word document, image and .md):
        convertToPdf(inputFile)
        

    ### To attach the pdf in email
        email(username, password, senderAddress, receiverAddress, subject, body, inputFile)
   