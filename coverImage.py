import fitz



def makeCoverImg(pdffile):
    doc = fitz.open(pdffile)

    page = doc.loadPage(0)  # number of page
    total_pages = doc.pageCount
    pix = page.get_pixmap()
    pdfName = pdffile.split("\\")[-1]
    if("\\"in pdffile):

        coverImg = pdffile.split("\\")[-1].split(".pdf")[0]+".png"
    else:
        coverImg =pdffile.split(".pdf")[0]+".png"
    pix.save(coverImg)
    print("Printing Pdf name and Total pages")
    print(f"{pdfName},{total_pages} Pages,{coverImg}")





 