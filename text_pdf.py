from pdfrw import PdfWriter
y = PdfWriter()
y.addpage(doc)
y.write('result.pdf')