#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Setup Environment
import openai
import pandas as pd
import streamlit as st


# In[ ]:


# Configure OpenAI API Key
openai.api_key = "Your_OpenAI_Key"  # Replace with your OpenAI key


# In[ ]:


# Define a function to generate a prompt for an AI data scientist
def generate_prompt(dataset_head, task_description):
    """
    This function generates a text prompt tailored for an AI data scientist. 
    The generated prompt includes a dataset snippet and a specific task 
    description, instructing the AI to respond with Python code.

    Parameters:
    - dataset_head (str): A string representation of the first few rows of the dataset. 
      Typically obtained using pandas DataFrame's `head()` method or similar.
    - task_description (str): A description of the task the AI needs to perform 
      using the provided dataset.

    Returns:
    - str: A formatted text prompt for the AI to interpret and act upon.
    """
    
    # Using an f-string to create a structured, context-specific prompt.
    # Including the dataset snippet (`dataset_head`) provides the AI with
    # context, while the `task_description` specifies the objective.
    prompt = f"""
You are an AI data scientist. The following is the first few rows of a dataset:
{dataset_head}

Your task is to: {task_description}

Respond with Python code for the task. Do not explain the code.
"""
    
    # Return the structured prompt as a string
    return prompt


# In[ ]:


# Function to Query OpenAI API
def get_llm_response(prompt):
    """
    This function interacts with the OpenAI API to generate a response from a language model.
    It takes a user-provided prompt as input, sends it to the OpenAI API, and retrieves the response.

    Args:
        prompt (str): The input text or query that will be passed to the language model.

    Returns:
        str: The content of the response generated by the OpenAI language model.
    """

    # Call the OpenAI ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Specify the model to use (e.g., GPT-3.5-turbo for high-quality results).
        
        # Define the conversation history for the chat-based language model.
        messages=[
            # Role of the system - Sets the behavior or persona of the model.
            {"role": "system", "content": "You are an AI data scientist."},

            # Role of the user - Provides the input prompt or question to the model.
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and return the generated response content from the API response object.
    # 'choices' contains the list of response options; here, we access the first choice's message content.
    return response['choices'][0]['message']['content']


# In[ ]:


# Main function to define the Streamlit app
def main():
    # Set the title of the app
    st.title("Feature Engineering Assistant")
    
    # Provide a description of the app's purpose
    st.write("Upload a dataset and define the feature engineering task.")

    # Section for uploading a dataset
    uploaded_file = st.file_uploader("Upload CSV Dataset", type="csv")  # File uploader widget for CSV files
    if uploaded_file:  # Check if a file is uploaded
        df = pd.read_csv(uploaded_file)  # Read the uploaded CSV file into a pandas DataFrame
        st.write("Dataset Preview:")  # Display a heading for the dataset preview
        st.dataframe(df.head())  # Show the first 5 rows of the dataset

        # Section for inputting a feature engineering task description
        task_description = st.text_area(
            "Describe the Feature Engineering Task",  # Prompt for the user
            "Create a new feature that indicates the day of the week from a date column named 'Order_Date'."  # Default text for guidance
        )

        # Generate Feature Engineering Code button
        if st.button("Generate Feature Engineering Code"):  # Button to trigger code generation
            # Convert the first 5 rows of the dataset into a string for context
            dataset_head = df.head().to_string()

            # Call a function to generate a prompt for the LLM
            prompt = generate_prompt(dataset_head, task_description)  # Pass dataset preview and task description
            st.write("Prompt Sent to LLM:")  # Display the generated prompt
            st.code(prompt, language="text")  # Show the prompt in a code block

            # Attempt to get the response from the LLM
            try:
                response = get_llm_response(prompt)  # Function to interact with the LLM and fetch generated code
                st.write("Generated Code:")  # Display heading for the generated code
                st.code(response, language="python")  # Show the Python code generated by the LLM

                # Optionally execute the generated code
                exec(response)  # Execute the generated Python code
                st.success("Code executed successfully! Check the transformed dataset.")  # Show success message
                st.dataframe(df.head())  # Display the transformed dataset
            except Exception as e:  # Handle errors during code execution
                st.error(f"An error occurred: {e}")  # Display error message

# Run the app when the script is executed
if __name__ == "__main__":
    main()

