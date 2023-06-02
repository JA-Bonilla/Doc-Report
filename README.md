# Doc-Report
Through the use of LLM's users are able to talk to their personal or company files to review documents quicker, find specific information, and generate reference based summaries, without the worry of data leaks. It runs off your computer!

This was built with [privateGPT](https://github.com/imartinez/privateGPT), [GPT4ALL](https://github.com/nomic-ai/gpt4all), [Langchain](https://github.com/hwchase17/langchain), [LlamaCpp](https://github.com/ggerganov/llama.cpp), [Tkinter-Designer](https://github.com/ParthJadhav/Tkinter-Designer), [Chromadb](https://www.trychroma.com/), [SentenceTransformers](https://www.sbert.net/), [Figma](www.figma.com), and [PDF2Image](https://pdf2image.readthedocs.io/en/latest/index.html).

![Screenshot of Doc-Report Output](/init/Doc-Report.png)

# Enviorment Setup
Due to the way Langchain loads SentenceTransformers an internet connection is required the first time `Gui.Py` is run.

In order to set your environment up to run the code here, first install all requirements:
`pip install -r requirements.txt`

In the Utils folder you will need to delete the name of the `enviorment.env` file so that you are left with just `.env`

-----------------------------------------

# System Requirements
## Python

This project works with Python 3.10 or later (though later versions are untested). Earlier versions of Python will not compile.

## System

It is recommended that this be run on a system that contains 16GB of memory or higher. Systems with 8GB of memeory experienced crashing.

Tested on system with the following specs:

CPU: Intel Core i7-10700

RAM: 16GB

## Average Time

Average response time based on Test System:

Avg Time for Ingest Preperation: 0:32 Mins (32 Seconds)

Avg Time for Response Generation: 1:41 Mins (101 Seconds)

-----------------------------------------

# Ingestion 
Uploaded documents, specifically PDF's, must be readable (Optical Character Recognition (OCR) funcionality must be applicable).

When running `Gui.py` click upload and a filedialog will open, requesting you to select a file. The default chosen document is PDF, however you can change the file type to the following:

- PDF File        (.PDF)
- CSV File        (.CSV)
- Word File       (.DOCX)
- PowerPoint File (.PPTX)
- Text File       (.TXT)

As documents are being ingested, a photo of the document will appear on the right and a user will be able to flip between pages of their document using the buttons above. Once ingestion is complete the red image next to the file name will turn green and you can proceed to communicate with your documents.

-----------------------------------------
# Response Generation

Once a question has been typed the user clicks the Generate button and your computer will begin to upload the AI model and process the data to generate an appropriate response for the user. Please note that this program can only run as fast as your computer's CPU can proccess. 

View System Requirements for average time info.

-----------------------------------------

# Mac with Intel CPU

When running a Mac with Intel hardware (not M1), you may run into clang: error: the clang compiler does not support '-march=native' during pip install.

If so set your archflags during pip install. eg: `ARCHFLAGS="-arch x86_64" pip3 install -r requirements.txt`

-----------------------------------------

# Disclaimer

This is a test project to validate the feasibility of a fully private solution for question answering using LLMs and Vector embeddings. It is not production ready, and it is not meant to be used in production. The models selection is not optimized for performance, but for privacy; but it is possible to use different models and vectorstores to improve performance.

-----------------------------------------

# Future Updates

- Resolve image resizing quality issue (Display a clearer image in the GUI).
- Add reference tabs (Allow users to understand what references the AI used, such as paragraph and page).
  - When reference tab is clicked, the page jumps to reference page. 
- Add loading bar for both ingestion and response generation.
- Format the GUI to be resizeable.
- Add page number input to jump to a specific page.
- Change Document Picture from button to label or changeable image.
- Co-processing to complete PDF-PNG conversion and ingestion at the same time (Reduce Ingestion Prep Time).

