import streamlit as st
from pathlib import Path
import google.generativeai as genai
import pandas as pd
from api_key import api_key

# Configure genai with api key
genai.configure(api_key=api_key)

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Apply safety measures  
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",  # Use the correct model name as required
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Define prompts for different sections
prompts = {
   "Soil Health Analysis": """
    As an agricultural expert, you are tasked with examining images of soil samples to assess soil health. Your expertise is crucial in providing recommendations for soil management and crop growth.

    Your Responsibilities include:

    1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying soil texture, color, and any visible signs of nutrient deficiency or contamination.
    2. Findings Report: Document all observed issues and indicators. Clearly articulate these findings in a structured format.
    3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including soil treatment and nutrient management.
    4. Intervention Suggestions: If appropriate, recommend possible interventions or strategies to improve soil health.

    Important Notes:

    1. Scope of Response: Only respond if the image pertains to soil health.
    2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
    3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with an Agricultural Expert before making any decisions."
    """,

    "Pest and Disease Detection": """
    As an agricultural expert, you are tasked with examining images of crops to identify pests and diseases. Your expertise is crucial in providing recommendations for pest management and disease control.

    Your Responsibilities include:

    1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying signs of pest infestation or disease.
    2. Findings Report: Document all observed issues and indicators. Clearly articulate these findings in a structured format.
    3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including pest control measures and disease management strategies.
    4. Intervention Suggestions: If appropriate, recommend possible interventions or treatments.

    Important Notes:

    1. Scope of Response: Only respond if the image pertains to crop health.
    2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
    3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with an Agricultural Expert before making any decisions."
    """,

    "Weather Forecasting": """
    As a climate expert, you are tasked with providing weather analysis and forecasts based on uploaded images of clouds or weather patterns. Your expertise is crucial in helping farmers plan their agricultural activities.

    Your Responsibilities include:

    1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying weather patterns and predicting potential weather changes.
    2. Findings Report: Document all observed weather indicators. Clearly articulate these findings in a structured format.
    3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including agricultural activities suited to the forecasted weather.
    4. Intervention Suggestions: If appropriate, recommend possible interventions or strategies to mitigate adverse weather impacts.

    Important Notes:

    1. Scope of Response: Only respond if the image pertains to weather patterns.
    2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
    3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Climate Expert before making any decisions."
    """
}

# Initialize the page configuration
st.set_page_config(page_title="Inside Home - Mother Nature", page_icon=":leaves:", layout="wide")

# Header
st.markdown("""
    <style>
    .header {
            background-color: #5F8575; /* Dark green */
            color: white;
            padding: 10px 0;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            position: sticky;
            top: 0;
            width: 100%;
            z-index: 1000;
        }

    .footer {
        background-color: #5F8575; /* Dark green */
        color: white;
        padding: 10px 0;
        text-align: center;
        font-size: 14px;
        position: sticky;
        bottom: 0;
        left: 0;
        width: 100%;
    }
    </style>
    <div class="header">
        <div>Empowering Farmers with GenAI</div>
    </div>
""", unsafe_allow_html=True)

# Set the logo
#st.image("nature_logo.jpg", width=704)


# Set the title
st.title("Gen AI - SmartFarm🌾")

# Set subtitle
st.subheader("GenNext Farming : Gemini AI-Powered Solutions for Soil, Crops, and Weather")

# Define initial state for posts and comments
if 'posts' not in st.session_state:
    st.session_state.posts = pd.DataFrame(columns=['username', 'title', 'content', 'comments'])

if 'current_user' not in st.session_state:
    st.session_state.current_user = 'Farmer'  # Example user, you could integrate user login functionality

# Function to add a new post
def add_post(username, title, content):
    new_post = pd.DataFrame([[username, title, content, []]], columns=['username', 'title', 'content', 'comments'])
    st.session_state.posts = pd.concat([st.session_state.posts, new_post], ignore_index=True)

# Function to add a comment to a post
def add_comment(post_index, comment):
    st.session_state.posts.at[post_index, 'comments'].append(comment)

# Function to generate content from the model
def generate_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

# Custom sidebar style
st.markdown("""
<style>
.sidebar .sidebar-content {
    background-color: #e1f5a9;  /* Light green, natural tone */
    padding: 20px;
    border-radius: 10px;
}

.sidebar .sidebar-content h2 {
    color: #2e7d32;  /* Dark green, earthy color */
    font-weight: bold;
}

.sidebar .sidebar-content button {
    background-color: #2e7d32;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
}

.sidebar .sidebar-content button:hover {
    background-color: #1b5e20;  /* Darker green for hover effect */
}
</style>
""", unsafe_allow_html=True)

# Tabs for navigation
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Home", "Soil Health Analysis", "Pest & Disease Detection", "Weather Forecasting","Chatbot", "Community Forum"])

# Display content based on the selected tab
with tab1:
    # st.subheader("Project Overview")

    st.write("### Project Title: Revolutionizing Agriculture with Gen AI")
    st.image("logo.jpg", width=704)  # Add your project image here

    st.write("### About the Project")
    st.write("SmartFarm integrates advanced AI models to offer comprehensive support to farmers. The application features tools for:")
    st.write("""
    <ul>
        <li>Analyzing soil health through image uploads</li>
        <li>Detecting pests and diseases in crops</li>
        <li>Forecasting weather patterns</li>
        <li>Chatbot</li>
    </ul>
    Each tool is designed to deliver precise and timely information, enabling farmers to make informed decisions that directly impact their crop yields and overall farm management.
    """, unsafe_allow_html=True)

    st.write("### Project Usefulness")
    st.write("""
    The SmartFarm application is designed to assist farmers, particularly in regions where agriculture plays a crucial role in the economy and livelihoods. Farmers often face significant challenges such as:
    <ul>
        <li>Poor soil health and fertility issues</li>
        <li>Unpredictable pest infestations and crop diseases</li>
        <li>Inaccurate weather information affecting crop planning and harvesting</li>
    </ul>
    SmartFarm tackles these challenges by providing an integrated platform that offers:
    <ul>
        <li>Detailed soil health analysis with tailored recommendations to improve soil quality and fertility</li>
        <li>Early detection of pests and diseases with actionable solutions to mitigate their impact</li>
        <li>Accurate weather forecasts to help farmers plan their agricultural activities effectively</li>
    </ul>
    By addressing these critical issues, SmartFarm aims to enhance farming practices, increase crop yields, and reduce resource wastage, leading to more efficient and sustainable agriculture. This positive change not only improves the lives of individual farmers but also contributes to food security and economic stability in agricultural communities.
    """, unsafe_allow_html=True)


    st.write("### Why I Chose This Topic")
    st.write("Agriculture is a critical sector, especially in developing regions where farmers face numerous challenges. The United States is a leading agricultural producer and supplier due to its land and natural resources. The agriculture sector, which includes farms and related industries, contributes 5.6% to the U.S. gross domestic product (GDP) and employs 10.4% of Americans. By leveraging technology, this project aims to address these challenges and provide practical solutions to improve farming efficiency and sustainability.")

    st.write("### Project Impact on Agriculture")
    st.write("The project is expected to have a significant positive impact on agriculture by enabling farmers to make informed decisions based on real-time data. This will enhance crop yield, improve soil management, and optimize resource usage, ultimately contributing to food security and economic development.")

with tab2:
    st.subheader("Soil Health Analysis Section")
    uploaded_file = st.file_uploader("Upload an image for Soil Health Analysis", type=["png", "jpg", "jpeg"], key="upload_image_soil_health")
    submit_button = st.button("Generate Soil Health Analysis", key="generate_analysis_soil_health")

    if submit_button:
        # Process the uploaded image
        if uploaded_file is not None:
            image_data = uploaded_file.getvalue()

            # Display the uploaded image
            st.image(image_data, caption="Uploaded Image", use_column_width=True)

            image_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": image_data
                },
            ]

            prompt_part = [
                image_parts[0],
                prompts["Soil Health Analysis"],
            ]
            # Generate response based on image and prompt
            analysis_response = generate_response(prompt_part)
            st.write(analysis_response)
        else:
            st.error("Please upload an image to analyze.")

with tab3:
    st.subheader("Pest and Disease Detection Section")
    uploaded_file = st.file_uploader("Upload an image for Pest and Disease Detection", type=["png", "jpg", "jpeg"], key="upload_image_pest_disease")
    submit_button = st.button("Generate Pest and Disease Detection Analysis", key="generate_analysis_pest_disease")

    if submit_button:
        # Process the uploaded image
        if uploaded_file is not None:
            image_data = uploaded_file.getvalue()

            # Display the uploaded image
            st.image(image_data, caption="Uploaded Image", use_column_width=True)

            image_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": image_data
                },
            ]

            prompt_part = [
                image_parts[0],
                prompts["Pest and Disease Detection"],
            ]
            # Generate response based on image and prompt
            analysis_response = generate_response(prompt_part)
            st.write(analysis_response)
        else:
            st.error("Please upload an image to analyze.")

with tab4:
    st.subheader("Weather Forecasting Section")
    uploaded_file = st.file_uploader("Upload an image for Weather Forecasting", type=["png", "jpg", "jpeg"], key="upload_image_weather_forecasting")
    submit_button = st.button("Generate Weather Forecasting Analysis", key="generate_analysis_weather_forecasting")

    if submit_button:
        # Process the uploaded image
        if uploaded_file is not None:
            image_data = uploaded_file.getvalue()

            # Display the uploaded image
            st.image(image_data, caption="Uploaded Image", use_column_width=True)

            image_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": image_data
                },
            ]

            prompt_part = [
                image_parts[0],
                prompts["Weather Forecasting"],
            ]
            # Generate response based on image and prompt
            analysis_response = generate_response(prompt_part)
            st.write(analysis_response)
        else:
            st.error("Please upload an image to analyze.")

with tab5:
    # Initialize the model and chat history
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])

    # Define function to get Gemini response
    def get_gemini_response(question):
        response = chat.send_message(question, stream=True)
        return response

    st.subheader("Gemini Chatbot")

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Display chat history
    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f"**{role}:** {text}")

    # User input field and submit button
    user_input = st.text_input("Ask the Gemini Chatbot:", key="user_input")
    if st.button("Send", key="send_message"):
        if user_input:
            # Add user message to chat history
            st.session_state['chat_history'].append(("You", user_input))

            # Generate response from Gemini model
            try:
                response = get_gemini_response(user_input)
                # Display response and add it to chat history
                response_text = ""
                for chunk in response:
                    response_text += chunk.text
                    st.write(f"**Gemini:** {chunk.text}")
                st.session_state['chat_history'].append(("Gemini", response_text))
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please enter a message.")


with tab6:
    st.subheader("Community Forum")

    if 'post_created' not in st.session_state:
        st.session_state.post_created = False

    if not st.session_state.post_created:
        st.sidebar.header("Community Forum")
        post_title = st.sidebar.text_input("Title", key="post_title")
        post_content = st.sidebar.text_area("Your Comments", key="post_content")

        if st.sidebar.button("Create Post"):
            if post_title and post_content:
                add_post(st.session_state.current_user, post_title, post_content)
                st.session_state.post_created = True
                st.sidebar.success("Post created successfully!")
            else:
                st.sidebar.error("Please fill in both title and content.")
    
    # Display posts
    st.subheader("All Posts")
    posts = st.session_state.posts
    for idx, post in posts.iterrows():
        st.write(f"**{post['username']}** - *{post['title']}*")
        st.write(post['content'])
        comments = post['comments']
        if comments:
            for comment in comments:
                st.write(f"    - {comment}")

        comment_input = st.text_input("Add a comment:", key=f"comment_input_{idx}")
        if st.button("Submit Comment", key=f"submit_comment_{idx}"):
            if comment_input:
                add_comment(idx, comment_input)
                st.experimental_rerun()  # Refresh to show new comment
            else:
                st.error("Please enter a comment.")


# Footer
st.markdown("""
    <div class="footer">
        <div>©2025 NikhilBhosale. All rights reserved.</div>
    </div>
""", unsafe_allow_html=True)

