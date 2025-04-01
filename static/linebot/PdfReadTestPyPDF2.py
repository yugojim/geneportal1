import PyPDF2 #使用PyPDF2讀圖片必須裝Pillow==9.4.0 pip install Pillow
import base64
import io
#import PIL.Image as Image
import matplotlib.pyplot as plt

pdffile="10.pdf"     #pdf檔路徑及檔名
# creating an object 
file = open(pdffile, 'rb')
# creating a pdf reader object
fileReader = PyPDF2.PdfFileReader(file)

# print the number of pages in pdf file
print(fileReader.numPages)
for page in fileReader.pages:
    print(page.extractText())
    
reader = PyPDF2.PdfReader(file)   
page = reader.pages[0]
count = 1
for image_file_object in page.images:
    with open(str(count) + image_file_object.name, "wb") as fp:
        ImageByte=image_file_object.data
        fp.write(ImageByte)
        fp.close()
        #ImageByteBase64 = base64.b64encode(image_file_object.data)
        #print(ImageByteBase64)
        #with open(str(count) + image_file_object.name + 'ImageByteBase64' ,'w+') as f:
            #f.write(ImageByteBase64.decode("utf-8"))
        #base64.b64decode(ImageByteBase64)
        #ImageImage=Image.open(io.BytesIO(ImageByte))
        #plt.imshow(ImageImage)
        count += 1
