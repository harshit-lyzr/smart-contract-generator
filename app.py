import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent,Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
api = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Smart Contract Generator",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# App title and introduction
st.title("Smart Contract Generator ₿⛓")
st.sidebar.markdown("### Welcome to the Lyzr Smart Contract Generator!")
st.sidebar.markdown("This app harnesses power of Lyzr Automata to Build Smart Contracts for WEB3 Projects. You have to Enter Contract Requirements and Contract Language and it will Generate Smart contract for your next Web3 Project")
st.markdown("This app uses Lyzr Automata Agent to Generate Smart Contract based on Contract details and language.")

open_ai_text_completion_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)

contract_det = st.sidebar.text_area("Enter Your Contract Details", height=200)
contract_language = st.sidebar.selectbox("Enter Contract Language", ("Solidity", "Vyper", "Ethereum", "Rust", "Move"))


def smart_contract(details,language):

    web3_agent = Agent(
            role="Blockchain expert",
            prompt_persona=f"Imagine you are an experienced Blockchain developer.Your Task is to generate Smart contract with given details."
        )

    prompt = f"""I am Building A project in {language}.The Description Of the project is below:
    description: {details}
    
    Your Task is to provide a code with all the requests above and no bugs.
    In your response provide all the code with notes and explanation of each function.
    
    Output:
    Smart Contract with code explanation
    [!Important] Do not Write code walk through or any thing else apart from the above
    """

    web3_task = Task(
        name="smart contract task",
        model=open_ai_text_completion_model,
        agent=web3_agent,
        instructions=prompt,
    )

    output = LinearSyncPipeline(
        name="Smart Contract Pipline",
        completion_message="Smart Contract Generated!!",
        tasks=[
              web3_task
        ],
    ).run()

    answer = output[0]['task_output']

    return answer


if st.sidebar.button("Generate", type="primary"):
    solution = product_description(contract_det,contract_language)
    st.markdown(solution)

