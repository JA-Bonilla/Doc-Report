import os
import sys
import ntpath
import subprocess
import shutil
import ctypes

import pdfreader

from pathlib import Path
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

from pdfreader import PDFDocument, SimplePDFViewer

from dotenv import find_dotenv, load_dotenv

import utils.AI
import utils.ingest

import aspose.words as aw

import  jpype     
import  asposecells

import aspose.slides as slides
import aspose.pydrawing as drawing

iterate = 0
pdf_fl = 0
Page = 0
load_path = "NULL"

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets")
SOURCE_PATH = OUTPUT_PATH / Path(r".\utils\source_documents")
INGEST_PATH = OUTPUT_PATH / Path(r".\utils\db")
INDEX_PATH = OUTPUT_PATH / Path(r".\utils\db\index")
JPG_PATH = OUTPUT_PATH / Path(r".\images")

poppler_path = r".\poppler-23.05.0\Library\bin"

load_dotenv(find_dotenv())



f_types = [('PDF Files', '*.pdf'), 
           ('CSV Files', '*.csv'),
           ('Word Doc File', '*.docx'),
           ('PowerPoint File', '*.pptx'),
           ('Text File', '*.txt')]

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def relative_to_images(path: str) -> Path:
    return JPG_PATH / Path(path)


def iteration():
    global iterate
    if iterate == 1:
        Generate()
        iterate = 0 
    else:
        window.after(1000, iteration)  # run again after 1000ms (1s)

def Upload_Clicked():
    global load_path, m_FileName, totalpages
    entry_1.config(state="normal")

    for f in os.listdir(JPG_PATH):
            os.remove(os.path.join(JPG_PATH, f))
    
    if load_path != "NULL":
        shutil.rmtree(INDEX_PATH)

        for f in os.listdir(INGEST_PATH):
            os.remove(os.path.join(INGEST_PATH, f))
    
    load_path = askopenfilename(filetypes=f_types)
    m_FileName = ntpath.basename(load_path)


    fd = open(load_path, "rb")
    doc = PDFDocument(fd)
    all_pages = [p for p in doc.pages()]
    totalpages = len(all_pages) - 1

    conv_JPG()

    shutil.copy(load_path, SOURCE_PATH)

    subprocess.run(["python", "utils\ingest.py"])

    for f in os.listdir(SOURCE_PATH):
        os.remove(os.path.join(SOURCE_PATH, f))

    entry_1.insert(0 , m_FileName)

    canvas.delete(image_6)
    entry_1.config(state="readonly")

def Pre_Gen():
    global iterate, load_path
    if load_path != "NULL":
        button_2.configure(image=button_image_3)
        iterate = 1
    else:
        ctypes.windll.user32.MessageBoxW(0, u"Please Upload a Document", u"Error!", 0)

def Generate():
    entry_3.config(state="normal")
    entry_3.delete(1.0, "end")

    query = entry_2.get(1.0,"end")

    answer = utils.AI.main(query=query)

    typeit(entry_3, "1.0", answer)

    button_2.configure(image=button_image_2)
    window.after(1000, iteration)  

def typeit(widget, index, string):
   entry_3.config(state="normal")
   if len(string) > 0:
      widget.insert(index, string[0])
      entry_3.config(state="disabled")
      if len(string) > 1:
         # compute index of next char
         index = widget.index("%s + 1 char" % index)

         # type the next character in half a second
         widget.after(25, typeit, widget, index, string[1:])

def conv_JPG():
    if ".pdf" in m_FileName:
        PDF2IMG()
        disp_PDF()
    elif ".csv" in m_FileName:
        asposeCSV()
    elif ".docx" in m_FileName:
        asposeDOC()
    elif ".pptx" in m_FileName:
        asposePPT()
    elif ".txt" in m_FileName:
        asposeTXT()

def disp_PDF():
    global pdf
    pdf = PhotoImage(file=relative_to_images("Output_new_0.png"))
    button_7.configure(image=pdf, bd=1)
    window.update()
    
def PDF2IMG():
    
    images = convert_from_path(load_path, output_folder=r".\images", dpi=500, poppler_path=poppler_path) #size=(552.5,715)

    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save(f'.\images\Output_'+ str(i) +'.png', 'png')
        output = Image.open(f'.\images\Output_'+ str(i) +'.png')
        new_out = output.resize((552, 715), Image.ANTIALIAS)
        new_out.save(f'.\images\Output_new_'+ str(i) +'.png', format='png')
    
def Right_Clicked():
    global pdf, Page
    Page = Page + 1
    if Page > totalpages:
        Page = 0
    pdf = PhotoImage(file=relative_to_images(f'Output_new_'+ str(Page) +'.png'))
    button_7.configure(image=pdf)
    window.update()

def Left_Clicked():
    global pdf, Page
    Page = Page - 1
    if Page < 0:
        Page = totalpages
    pdf = PhotoImage(file=relative_to_images(f'Output_new_'+ str(Page) +'.png'))
    button_7.configure(image=pdf)
    window.update()


def asposeCSV():
    jpype.startJVM()
    from asposecells.api import Workbook
    workbook = Workbook(load_path)
    workbook.save("Output.jpg")
    jpype.shutdownJVM()

def asposeDOC():
    doc = aw.Document(load_path)
          
    for page in range(0, doc.page_count):
        extractedPage = doc.extract_pages(page, 1)
        extractedPage.save(f"Output_{page + 1}.jpg")

def asposePPT():
    pres = slides.Presentation(load_path)

    for index in range(pres.slides.length):
        # Get reference of slide
        slide = pres.slides[index]

        # Save as JPG
        slide.get_thumbnail().save("slide_{i}.jpg".format(i = index), drawing.imaging.ImageFormat.jpeg)

def asposeTXT():
    doc = aw.Document(Input.txt)
          
    for page in range(0, doc.page_count):
        extractedPage = doc.extract_pages(page, 1)
        extractedPage.save(f"Output_{page + 1}.jpg")









window = Tk()

window.geometry("1080x900")
window.configure(bg = "#3B3B3B")
window.title("Doc-Report")
window.iconbitmap(r".\ICON.ico")

canvas = Canvas(
    window,
    bg = "#3B3B3B",
    height = 900,
    width = 1080,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    background="#3C3C3C",
    command=lambda: Upload_Clicked(),
    activebackground="#3C3C3C",
    relief="flat"
)
button_1.place(
    x=20.0,
    y=65.0,
    width=135.0,
    height=56.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    284.5,
    93.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Consolas", 14)
)
entry_1.place(
    x=168.5,
    y=68.0,
    width=232.0,
    height=40.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    225.0,
    256.0,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Bahnschrift", 14),
    wrap='word'
)
entry_2.place(
    x=30.0,
    y=170.0,
    width=395.0,
    height=110.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Pre_Gen(),
    relief="flat"
)
button_2.place(
    x=239.0,
    y=278.0,
    width=184.0,
    height=56.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    225.0,
    627.0,
    image=entry_image_3
)
entry_3 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Bahnschrift", 14),
    wrap='word'
)
entry_3.place(
    x=30.0,
    y=419.0,
    width=395.0,
    height=400.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    765.0,
    450.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    764.0,
    450.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    67.0,
    400.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    73.0,
    152.0,
    image=image_image_4
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    background="#626262",
    command=lambda: Left_Clicked(),
    activebackground="#626262",
    relief="flat"
)
button_4.place(
    x=726.0,
    y=18.0,
    width=35.0,
    height=40.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    background="#626262",
    command=lambda: Right_Clicked(),
    activebackground="#626262",
    relief="flat"
)
button_5.place(
    x=768.0,
    y=18.0,
    width=35.0,
    height=40.0
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    420.0,
    93.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    420.0,
    93.0,
    image=image_image_6
)

pdf = PhotoImage(
    file=relative_to_images(r"..\temp.png"))
button_7 = Button(
    image=pdf,
    borderwidth=0,
    highlightthickness=0,
    background="#D9D9D9",
    command=lambda: print("button_5 clicked"),
    activebackground="#D9D9D9",
    bd=0,
    relief="solid",
    
)
button_7.place(
    x=488.0,
    y=85.0,
    width=552.5,
    height=715
)




window.after(1000, iteration)
window.resizable(False, False)
window.mainloop()
