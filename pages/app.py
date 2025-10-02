import streamlit as st
import numpy as np
import requests
import base64
import os
from PIL import Image
from supabase import create_client

from file_upload import upload_file, download_file, record_logo_entry, fetch_accounts, fetch_logos_for_account, render_logo_gallery



if not st.user.is_logged_in:
    st.error("Please log in to access the App")
    st.stop()

ENDPOINT_URL = 'https://askai.aiclub.world/27a37a06-93bd-4ec5-a56c-963adc53c0e7'


BUCKET_NAME = st.secrets.get("SUPABASE_BUCKET", "Butterfly_Classification")
TABLE_NAME = st.secrets.get("SUPABASE_TABLE", "account_logos")
SUPPORTED_TYPES = ["png", "jpg", "jpeg", "gif"]
IMAGE_NAME = "user_image.png"

#####functions#########
def get_prediction(image_data, url):
  r = requests.post(url, data=image_data)
  response = r.json()
  print(response)
  return response

  

#Building the website

#title of the web page
st.title("Butterfly Classifer")

client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
#setting the main picture
st.image(
    "https://t4.ftcdn.net/jpg/10/09/58/79/360_F_1009587933_xfLSLUHWaMJDnhvB6rJFtYZosRs0ObNr.jpg", 
    caption = "Butterfly")

#about the web app
st.header("About the Web App")

#details about the project
with st.expander("Web App 🌐"):
    st.subheader("Butterfly Image Predictions")
    st.write("This web app is about.....................")

#setting the tabs
tab1, tab2 = st.tabs(['Image Upload 👁️', 'Camera Upload 📷'])

#tab1
with tab1:
    #setting file uploader
    #you can change the label name as your preference
    image = st.file_uploader(label="Upload an image",accept_multiple_files=False, help="Upload an image to classify them")



    if image:
        #validating the image type
        
        # image_type = image.type.split("/")[-1]
        # if image_type not in ['jpg','jpeg','png','jfif']:
        #     st.error("Invalid file type : {}".format(image.type), icon="🚨")
        # else:
            #displaying the image
            user_image = Image.open(image)
            # save the image to set the path
            user_image.save(IMAGE_NAME)
            IMG_NAME = image.name 
            st.image(user_image, caption = "Uploaded Image")

            #getting the predictions
            with image:
                data_bytes = image.read()
                payload = base64.b64encode(data_bytes)
                response = get_prediction(payload, ENDPOINT_URL)
                st.success(f"Class Label: {response}")
                #account_id = response
                submitted = st.button("Upload to DB")

            if submitted:
                upload_file(client, user_image, account_id = 'Dogs', image_name = IMG_NAME, data = data_bytes)
                # if not account_id:
                #     st.warning("Enter an account ID before uploading.")
                
                
                # elif uploaded_file is None:
                #     st.warning("Choose a logo file to upload.")
                # else:
                #     storage_path = upload_file(client, uploaded_file, account_id)
                #     if storage_path:
                #         stored = record_logo_entry(
                #             client,
                #             account_id,
                #             uploaded_file.name,
                #             storage_path,
                #         )
                #         if stored:
                #             st.success(f"Stored logo '{uploaded_file.name}' for account '{account_id}'.")
            
        


with tab2:
    #camera input
    cam_image = st.camera_input("Please take a photo")

    if cam_image:
        #displaying the image
        st.image(cam_image)

        #getting the predictions
        with cam_image:
            payload = base64.b64encode(image.read())
            response = get_prediction(payload, ENDPOINT_URL)
            
            #displaying the predicted label
            st.success("Your Condition is **{}**".format(label))
            
