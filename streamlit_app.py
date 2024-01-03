import os
import shutil
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException
import openai
import facebook
from selenium.webdriver.chrome.options import Options
import requests
from openai import OpenAI
from monsterapi import client
import schedule
import threading
from datetime import datetime, timedelta
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import pytz 
from datetime import datetime, timezone
import os
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
OPENAI_API_KEY = st.secrets['OPENAI_API_KEY'] 

# write all the functions here and include @st.cache_resource(show_spinner=False) before def line
        
@st.cache_resource(show_spinner=False)
def get_logpath():
    return os.path.join(os.getcwd(), 'selenium.log')


@st.cache_resource(show_spinner=False)
def get_chromedriver_path():
    return shutil.which('chromedriver')


@st.cache_resource(show_spinner=False)
def get_webdriver_options():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")
    return options


def get_webdriver_service(logpath):
    service = Service(
        executable_path=get_chromedriver_path(),
        log_output=logpath,
    )
    return service


def delete_selenium_log(logpath):
    if os.path.exists(logpath):
        os.remove(logpath)


def show_selenium_log(logpath):
    if os.path.exists(logpath):
        with open(logpath) as f:
            content = f.read()
            st.code(body=content, language='log', line_numbers=True)
    else:
        st.warning('No log file found!')


def run_selenium(logpath):
    browsers=webdriver.Chrome(options=get_webdriver_options(), service=get_webdriver_service(logpath=logpath))
        
        
    return browsers


if __name__ == "__main__":
    logpath=get_logpath()
    delete_selenium_log(logpath=logpath)
    browser=run_selenium(logpath=logpath)
    st.set_page_config(page_title="FB Automate", page_icon='✅',
        initial_sidebar_state='collapsed')
    st.title('Facebook Posts Automation')
    st.markdown('---')

    st.balloons()
    login_option = st.sidebar.selectbox("Choose login option:", ("Select", "Admin login", "User login"))

    if login_option == "Select":
        st.warning("Please select a login option.")

    elif login_option == "Admin login":
        st.warning("Admin login feature is not implemented yet.")
        # You can add admin login functionality here if needed.

    elif login_option == "User login":
        # User credentials step
        if st.checkbox('Existing user'):
            st.subheader("User Credentials")
            user_username = st.text_input("Enter your username")
            user_password = st.text_input("Enter your password", type="password")

            if st.checkbox("Validate User Credentials"):
                if validate_user_credentials(user_username, user_password):
                    st.success("User credentials validated successfully!")

                    # Facebook login and profile selection step
                    st.subheader("Facebook Login and Profile Selection")
                    #facebook_username = st.text_input("Enter your Facebook username")
                    #facebook_password = st.text_input("Enter your Facebook password", type="password")
                    App_name = st.text_input("Enter your Facebook App Name")
                    #restuarant_name=st.text_input("Enter Your Resturant name")
                    nature_of_cuisine=st.text_input("Enter Nature of Cuisine")
                    occasion=st.text_input("Enter the occasion")
                    offer=st.text_input("Enter the offer or the discount")
                    other_keywords=st.text_input("Enter keywords to describe the image / poster you want to post")
                    location=st.text_input("Enter your location")
                    if st.checkbox("Run"):
                        login_to_facebook_existing_user(App_name,restuarant_name,location,nature_of_cuisine,occasion,offer,other_keywords)
                else:
                    st.error("Invalid user credentials. Please try again.")
        if st.checkbox('New user'):
            st.subheader("User Credentials")
            user_username = st.text_input("Enter your username")
            user_password = st.text_input("Enter your password", type="password")

            if st.checkbox("Validate User Credentials"):
                if validate_user_credentials(user_username, user_password):
                    st.success("User credentials validated successfully!")

                    # Facebook login and profile selection step
                    st.subheader("Details to post")
                    #facebook_username = st.text_input("Enter your Facebook username")
                    #facebook_password = st.text_input("Enter your Facebook password", type="password")
                    App_name = st.text_input("Enter your Facebook App Name")
                    restuarant_name=st.text_input("Enter Your Resturant name")
                    nature_of_cuisine=st.text_input("Enter Nature of Cuisine")
                    occasion=st.text_input("Enter the occasion")
                    offer=st.text_input("Enter the offer or the discount")
                    other_keywords=st.text_input("Enter keywords to describe the image / poster you want to post")
                    location=st.text_input("Enter your location")
                    if st.checkbox("Run"):
                        login_to_facebook(App_name,restuarant_name,location,nature_of_cuisine,occasion,offer,other_keywords)      
                else:
                    st.error("Invalid user credentials. Please try again.")

