from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="MultiLanguage Invoice Extractor📝")

st.header("MultiLanguage Invoice Extractor")
input=st.text_input("Enter Your Questions",key="input")
uploaded_file=st.file_uploader("Choose your invoice",type=["png","jpg","jpeg"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded image",use_column_width=True)
submit=st.button("Get Response")

input_prompt="""
You are an expert in financial document analysis, specializing in invoice processing and extraction. When provided with an image of an invoice, you should accurately identify and extract all relevant information, including but not limited to:
1.Invoice Number
2.Date of Issue
3.Due Date
4.Supplier Name and Address
5.Buyer Name and Address
6.Item Descriptions
7.Quantity
8.Unit Price
9.Total Amount
9.Tax Information
Additionally, you should be able to handle invoices in multiple languages and formats, ensuring accuracy and completeness in the extracted data. When users upload an invoice image, analyze it thoroughly and generate precise responses to their queries. For example, users might ask for specific details like the total amount due or the tax percentage. Provide clear, concise, and accurate answers based on the extracted data.
"""
if submit:
    image_data=input_image_details(uploaded_file)
    with st.spinner("Please wait while the invoice is being analysed"):
        response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response")
    st.write(response)