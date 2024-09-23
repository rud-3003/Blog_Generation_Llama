import streamlit as st
from langchain.prompts import PromptTemplate
from ctransformers import AutoModelForCausalLM  # Ensure this is the correct import

# Function to get response from Llama 2 model
def getLlamaresponse(input_text, no_words, blog_style):
    # Llama 2 Model - Loading the model
    llm = AutoModelForCausalLM.from_pretrained("models/llama-2-7b-chat.ggmlv3.q8_0.bin", 
                                               model_type="llama")
    
    # Prompt Template
    template = """
    Write a blog for a {blog_style} job profile on the topic "{input_text}" within {no_words} words.
    """
    
    prompt = PromptTemplate(input_variables=["blog_style", "input_text", "no_words"],
                            template=template)
    
    # Generate the formatted prompt string
    formatted_prompt = prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words)
    
    # Generate the response from Llama 2 model
    response = llm(formatted_prompt, 
                   max_new_tokens=int(no_words),   # Set max new tokens directly
                   temperature=0.01)               # Set temperature directly
    
    # Print response for debugging
    print(response)
    
    return response

# Streamlit page setup
st.set_page_config(page_title="Generate Blogs", page_icon="🤖", layout="centered")

st.header("Generate Blogs 🤖")

# Input fields in Streamlit
input_text = st.text_input("Enter the Blog Topic")

# Creating two more columns for additional fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input("No of Words")  # No of words is a string initially

with col2:
    blog_style = st.selectbox("Writing the blog for", ("Researchers", "Data Scientist", "Common People"), index=0)

submit = st.button("Generate")

# Final response
if submit:
    if input_text and no_words.isdigit():  # Ensure the no_words input is valid
        st.write(getLlamaresponse(input_text, int(no_words), blog_style))  # Convert no_words to int
    else:
        st.error("Please enter a valid topic and number of words.")
