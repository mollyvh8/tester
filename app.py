# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 16:42:36 2023

@author: molly
"""
# Import necessary libraries
import streamlit as st
from PyPDF2 import PdfReader
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # Add this import
from selenium.webdriver.support import expected_conditions as EC  # Add this import
import os

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = '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'

def main():

    # Configure Streamlit page settings
    st.set_page_config(page_title="Ask Moll.AI and Bern.AI")

    # Create a header for the Streamlit app
    st.header("Moll.AI and Bern.AI: Your Virtual Career Coaches💬")

    # Inputs for job search
    st.subheader("Step 1: Search for Jobs")
    job_title_input = st.text_input("Enter desired job title")
    job_location_input = st.text_input("Enter job location")

    def scrape_indeed(job_title, job_location):
        job_listings = []
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
    
        formatted_job_title = job_title.replace(' ', '+')
        formatted_job_location = job_location.replace(' ', '+')
        url = f'https://www.indeed.com/jobs?q={formatted_job_title}&l={formatted_job_location}'
    
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "jobTitle")))
    
        try:
            jobs = driver.find_elements(By.CLASS_NAME, "jobTitle")
            if not jobs:
                print("No jobs found on the page")
            for job in jobs[:15]:
                job_link_element = job.find_element(By.CSS_SELECTOR, "a")
                job_title = job_link_element.find_element(By.CSS_SELECTOR, "span").get_attribute("title")
                job_link = job_link_element.get_attribute("href")
                job_listings.append((job_title, job_link))
        except Exception as e:
            print("An error occurred:", e)
    
        driver.quit()
        return job_listings
    
    # Button to trigger job search
    if st.button('Search Jobs'):
        if job_title_input and job_location_input:
            job_listings = scrape_indeed(job_title_input, job_location_input)
            if job_listings:
                for title, link in job_listings:
                    st.markdown(f"[{title}]({link})", unsafe_allow_html=True)
            else:
                st.write("No job listings found.")
        else:
            st.write("Please enter both job title and location.")

    st.subheader("Step 2: Upload Your Resume and Enter Job Description")
    # File uploader widget for the resume PDF
    resume_file = st.file_uploader("Upload your Resume", type="pdf")
    resume_text = ""
    if resume_file is not None:
        pdf_reader = PdfReader(resume_file)
        for page in pdf_reader.pages:
            resume_text += page.extract_text()

    # Get the job description text 
    job_description_text = st.text_area("Enter the Job Description")
    
    # Check if both resume and job description have been uploaded
    if resume_text and job_description_text:
        # Initialize the language model
        llm = OpenAI(model_name='text-davinci-003')

        # Define the template for resume improvement suggestions
        resume_improvement_template = '''
        Resume: {resume_text}

        Job Description: {job_description_text}

        Suggest specific improvements to make the resume more aligned with the job description.
        '''

        # Create the PromptTemplate object for resume improvements
        resume_improvement_prompt = PromptTemplate(
            input_variables=['resume_text', 'job_description_text'],
            template=resume_improvement_template
        )

        # Generate the resume improvement prompt
        final_resume_improvement_prompt = resume_improvement_prompt.format(
            resume_text=resume_text, 
            job_description_text=job_description_text
        )

        # Print the final prompt and the language model's response for resume improvement
        print(final_resume_improvement_prompt)
        # Uncomment the next line to run it with the language model
        print(llm(final_resume_improvement_prompt))

        # Generate and display the resume improvement suggestions
        resume_improvement_output = llm(final_resume_improvement_prompt)
        st.subheader("Resume Improvement Suggestions:")
        st.text_area("Suggestions", resume_improvement_output, height=150)

        # Define the template for generating a cover letter
        cover_letter_template = '''
        Create a cover letter for the applicant with the resume below, targeting the job described in the job description:

        Applicant's Resume:
        {resume_text}

        Target Job Description:
        {job_description_text}
        '''

        # Create the PromptTemplate object for the cover letter
        cover_letter_prompt = PromptTemplate(
            input_variables=['resume_text', 'job_description_text'],
            template=cover_letter_template
        )

        # Generate the cover letter prompt
        final_cover_letter_prompt = cover_letter_prompt.format(
            resume_text=resume_text, 
            job_description_text=job_description_text
        )

        # Print the final prompt and the language model's response for the cover letter
        print(final_cover_letter_prompt)
        # Uncomment the next line to run it with the language model
        print(llm(final_cover_letter_prompt))
        # Generate and display the cover letter
        cover_letter_output = llm(final_cover_letter_prompt)
        st.subheader("Sample Cover Letter:")
        st.text_area("Cover Letter", cover_letter_output, height=300)

# Run the main function when the script is executed
if __name__ == '__main__':
    main()
