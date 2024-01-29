'''
Entry-point for Streamlit application, all the pages are located in pages/ folder
'''

import streamlit as st

# Entry point to run the web application
def main():
    st.set_page_config(page_title="Welcome!", page_icon="📚")

    st.title("Welcome to the Book Browser")
    st.write("Explore and discover your next favorite book!")

if __name__ == "__main__":
    main()
