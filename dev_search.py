from dotenv import load_dotenv
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import os
import time
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import pandas as pd  
import time



if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

if "Request to Contact" not in st.session_state:
    st.session_state["Request to Contact"] = False

def main():
    load_dotenv()
    st.set_page_config(layout="centered", page_icon = "rocket")
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    css="""
    <style>
    [data-testid="stForm"] {
        background: #32196d
    }
    [data-testid="stImage"]{
        clip-path:circle();
        width:150px;
        height:150px;
        margin-left: auto;
        margin-right: auto;
    }
    [data-testid="StyledLinkIconContainer"]{
        text-align: center;
    }
    [data-testid="stLinkButton"]{
        text-align: center;
    }
   
    [data-testid="column"] {
    
    box-shadow: rgb(0 0 0 / 20%) 0px 2px 1px -1px, rgb(0 0 0 / 14%) 0px 1px 1px 0px, rgb(0 0 0 / 12%) 0px 1px 3px 0px;
    border-radius: 15px;
    padding: 2% 2% 2% 2%;
    align-items: center;
    background: #32196d
    
} 

    </style>
"""
    st.write(css, unsafe_allow_html=True)
    page_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://images.unsplash.com/photo-1557683304-673a23048d34?q=80&w=1700&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-repeat: no-repeat;
        background-size: cover;
        }}
        </style>
        """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
   
      
    st.header("Let's Find You an A.I. Professional :rocket: ", anchor= False)
    st.divider()
    st.subheader('We will scout the :blue[WEB] to find you exactly who you are looking for :male-detective: \n\n', anchor= False)

    #API_KEY = os.getenv("OPENAI_API_KEY")
    
    chat_llm = ChatOpenAI(temperature=0.0, openai_api_key=os.getenv('OPENAI_API_KEY'))

    #url = "https://docs.google.com/spreadsheets/d/1_JsZEuAk7ikUgqy4MRj57xpra1XcDzu2Fu2GSRIBp3c/edit?usp=sharing"

    conn = st.experimental_connection("gsheets", type=GSheetsConnection)

    df = conn.read(worksheet = "Sheet1",  usecols=[0, 1, 2, 3])
    df_form = conn.read(worksheet = "Sheet2", usecols=list(range(2)), ttl=5)
    df_form = df_form.dropna(how="all")
    

    agent = create_pandas_dataframe_agent(ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106", openai_api_key=os.getenv('OPENAI_API_KEY')),df,agent_type=AgentType.OPENAI_FUNCTIONS,)
    
    
    
    
    with st.form("my_form"):
        st.subheader("Please fill out your :blue[name, email] and your :blue[industry]", anchor= False)
        form_name = st.text_input("What is your Name ?",placeholder="name")
        form_email = st.text_input("What's your email ?", placeholder="email")
        option = st.selectbox('Provide Your Industry',
        ('Real Estate', 'Financial Services', 'E-Commerce'), index= None)
        st.write('You selected:', option)
        st.divider()
        st.subheader("Now tell us more about :blue[WHO] you are trying to find", anchor= False)
        prompt_1 = st.text_area(" ",placeholder="I need an AI consultant for my business profiecient in Zapier and CRM.", max_chars=100)
        if st.form_submit_button("Submit"):
            if not form_name or not form_email:
                st.warning("Ensure all mandatory fields are filled.")
                st.stop()
            elif form_email in df_form['email']:
                st.warning("This email has been already registered")
                st.stop()
            else:
                df_submitted = pd.DataFrame(
                    [
                        {
                            "name": form_name,
                            "email": form_email,
                        }
                    ]
                )
                st.session_state["submitted"] = not st.session_state["submitted"]
                updated_df = pd.concat([df_form, df_submitted], ignore_index=True)
            
                # Update Google Sheets with the new vendor data
            conn.update(worksheet="Sheet2", data=updated_df)
            
            

    
    ID = ResponseSchema(name="ID",description="This is ID of the worker")



    response_schemas = [ID]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        
    format_instructions = output_parser.get_format_instructions()
        
    
    
    
    try:
        if st.session_state["submitted"]:
            
            
            output=agent.run(f"{prompt_1}. Choose any and return ID of this person. Explain your choice.")
            time.sleep(3)
            #print(format_instructions)
            template_string = """

            Take the text below delimited by triple backticks and use it to extract ID.

            text: ```{output}```
            
            ```{format_instructions}```
        
            """     
            prompt_template = ChatPromptTemplate.from_template(template= template_string)
            branding_messages = prompt_template.format_messages(output=output, format_instructions=format_instructions)
            consultant_response = chat_llm(branding_messages)
            response_as_dict = output_parser.parse(consultant_response.content)
            print(response_as_dict)
            num=response_as_dict['ID']
            sql = f'''
            SELECT *
            FROM Sheet1
            WHERE ID = {num};'''
            df_workers = conn.query(worksheet = "Sheet1", sql=sql)
            #st.dataframe(df_worekers)
            #df_workers["Image"]="https://static.streamlit.io/examples/cat.jpg"
            df = df_workers[["Image","Name","Pay per hour", "Description", "Success Rate", "Experience"]]
            
            
            
            with st.status("Looking for a candidate..."):
                time.sleep(2)
            #st.markdown(output)
            container = st.container()
            
            col1, col2 = st.columns([2, 5])
            with container:
                with col1:
                    st.header("Info ", anchor= False)
                    st.divider()
                    st.image(f"{df['Image'][0]}")
                    st.subheader(f":blue[{df['Name'][0]}]", anchor= False)
        
                    #if prompt_1 is not None:
                    st.link_button("Request to Contact", f"https://mail.google.com/mail/u/1/?view=cm&to=info@lorenzo-llm.com&su=Automation Project&body=Hey there! I am curious to discuss further details with {df['Name'][0]}")
                    st.divider()
                    st.header("Pay: ", anchor= False)
                    st.subheader(f":blue[{df['Pay per hour'][0]}]", anchor= False)
                    st.header("Earned: ", anchor= False)
                    st.subheader(f":blue[{df['Experience'][0]} earned]",  anchor= False)
                    st.header("Review :", anchor= False)
                    st.subheader(f":blue[{df['Success Rate'][0][0:4]} Positive]",  anchor= False)
        
                with col2:
                    st.header("Description", anchor= False)
                    st.divider()
                    st.write(f"{df['Description'][0]}")
    except :
        st.write(":pleading_face: OOOPS something went wrong, please try rephrasing your prompt")
        
        
        
    
if __name__ == '__main__':
    main()

# example/st_app.py

