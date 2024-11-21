import uuid

import streamlit as st
from langserve import RemoteRunnable
from pprint import pprint

from langchain_core.messages import HumanMessage

st.title("Welcome to Investor's Diary!")
input_text = st.text_input('What can i do??? You can ask me to add a new stock (BUY/SELL) transactions, Analyse your transaction history so far, for each transactions you can have your justification note or thought process which further you can ask specific question on your personal choice, above that you can do detailed research on a company.')

if input_text:
    with st.spinner("Processing..."):
        try:
            app = RemoteRunnable("http://localhost:8000/diary/")
            thread_id = str(uuid.uuid4())

            config = {
                "configurable": {
                    "thread_id": thread_id,
                }
            }

            print(thread_id, config, input_text)
            for output in app.stream({"messages":[input_text]},
                                     config,
                                     stream_mode="values"):
                print(output)
                for key, value in output.items():
                    # Node
                    pprint(f"Node '{key}':")
                    # Optional: print full state at each node
                    pprint.pprint(value["keys"], indent=2, width=80, depth=None)
                pprint("\n---\n")
            output = value['generation']  
            st.write(output)
        
        except Exception as e:
            st.error(f"Error: {e}")