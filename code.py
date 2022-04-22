
# import required modules


import os
import shutil
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient, BlobServiceClient
from azure.storage.blob import ContainerClient

from pdf2image import convert_from_path
from pytesseract import image_to_string

# storrage account url
account_url = "https://ourdemostorage.blob.core.windows.net/"


# authenticating the account
creds = DefaultAzureCredential()
service_client = BlobServiceClient(
    account_url=account_url,
    credential=creds
)


# pdfContainer = service_client.get_container_client("bengolipdfcontainer")

# creating connection string
co = "DefaultEndpointsProtocol=https;AccountName=ourdemostorage;AccountKey=9gbhPvg8cUnPYvSoaBnZc1cE90CFkAsAkMwkeP2yN+MT5xHAUbSLglVJ1YAvp0ElDqmHJ7HcMOfb+AStS6gQqw==;EndpointSuffix=core.windows.net"


# getting the client pdf container(fetching the pdf for OCR operations )
# txtContainer = ContainerClient.from_connection_string(conn_str = co, container_name="bengolitxtcontainer")


# getting  the client text container(for uploading the text files that have been converted via OCR)
txtContainer = ContainerClient.from_connection_string(
    conn_str=co, container_name="bengolitxtcontainer")




# getting  the client pdf container(for converting the pdf files that have been uploaded)
pdfContainer = ContainerClient.from_connection_string(
    conn_str=co, container_name="bengolipdfcontainer")


# /**
#   * @author pranav
#   *
#   * this function takes container as a parameter and returns
#     a list of blob text file names that are present in a container.
#   */
def gettingAllTxtBlobs(container):
    print("Getting all Text files from the bengoli txt Container")
    l = []
    # flag = True
    blobTxtList = container.list_blobs()
    for blobText in blobTxtList:
        l.append(blobText.name)
    else:
        if not (len(l) > 0):
            print("Container is Empty")
    print("COMPLETED")
    return l


# /**
#   * @author pranav
#   *
#   * this function takes container as a parameter and returns
#     a list of blob pdf file names that are present in a container.
#   */
def gettingAllPdfBlobs(container):
    print("Getting all pdf files from the bengoli txt Container")
    l = []
    # flag = True
    blobpdfList = container.list_blobs()
    for blobPdf in blobpdfList:
        l.append(blobPdf.name)
    else:
        if not (len(l) > 0):
            print("BengoliTextContainer is Empty")
    print("COMPLETED")
    return l


# it contains list of text files from the bengolitextContainer
txtList = gettingAllTxtBlobs(txtContainer)


# it contains list of pdf files from the bengolipdfContainer
pdfList = gettingAllPdfBlobs(pdfContainer)


# path folder where pdf will be saved
folder = r"D:\19042022\pdf"
def downloadBlob(filename):
    print(f"Downloading {filename}")
    blob = BlobClient.from_connection_string(
        conn_str=co, container_name="bengolipdfcontainer", blob_name=filename)
    with open(folder+"\\"+filename, "wb") as my_blob:
        blob_data = blob.download_blob()
    
        blob_data.readinto(my_blob)
        print("COMPLETED")

txtNList = [file.strip(".txt") for file in txtList]

for pdf in pdfList:# silicing is needed for .pdf and .txt-----------------------------------
    pdfn = pdf.strip(".pdf")
    if pdfn not in txtNList:
       
        downloadBlob(pdf)



# folder location to store the downloaded pdf

def convert_pdf_to_img(pdf_file):
    return convert_from_path(pdf_file)


def convert_image_to_text(pdf_file):
    text = image_to_string(pdf_file, lang="eng")
    return text


def get_text_from_any_pdf(pdf_file):
    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    for pg, img in enumerate(images):
        final_text += convert_image_to_text(img)
    return final_text


dirName = "text"
for file in os.listdir(folder) :
    if os.path.isfile(os.path.join(folder,file)):
        print("Performing OCR on")
        print(f"{file}")
        data = get_text_from_any_pdf(folder+"\\"+file)

        if not (os.path.isdir(os.path.join(folder,dirName))):
            print("making folder :text")
            os.mkdir(folder+"\\"+dirName)
            with open(folder+"\\"+dirName+"\\"+file+".txt","w+") as f:
                print("Writing data into text file")
                f.write(data)
        elif(os.path.isdir(os.path.join(folder,dirName))):
            full_path = os.path.join(folder,dirName)
            with open(full_path+"\\"+file.strip(".pdf")+".txt","w+") as f:
                print("Writing data into text file")
                f.write(data)


# uploading files after performing ocr
flag = True
for file in os.listdir(os.path.join(folder,dirName)) :
    if flag:
        os.chdir("pdf/text")
        flag = False
    if os.path.isfile(file):
        blob = BlobClient.from_connection_string(conn_str=co, container_name="bengolitxtcontainer", blob_name=file)
        with open(os.path.abspath(file), "rb") as data:
            print("uploading the text file")
            print(f"{file}")
            blob.upload_blob(data)
            print("COMPLETED")



# delete all the files in the folder that has been downloaded
def clearData(pathPara):
    if (os.path.isfile(pathPara)):
        print("Removing file")
        os.remove(pathPara)
        print("COMPLETED")
    elif(os.path.isdir(pathPara)):
        print("Removing folder")
        shutil.rmtree(pathPara,ignore_errors=True)
        print("COMPLETED")

    

for file in os.listdir(folder):
    clearData(os.path.join(folder,file))