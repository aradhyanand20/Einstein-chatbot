from dotenv import load_dotenv
import os
import gradio as gr
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

system_prompt = """ You are albert enistein  and reply just like him using humor and all the life experiences he had based on it.Answer in 2-6 sentences
"""
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key =gemini_key,
    temperature = 0.4
)
prompt = ChatPromptTemplate.from_messages([
     ("system", system_prompt),
     (MessagesPlaceholder(variable_name = "history")),
     ("user","{input}")]
)

chain = prompt | llm | StrOutputParser()
history = []
print("This is Albert, how can I help you")
def chat(user_input,hist):
    print(user_input,hist)
    langchain_history =[]
    for item in hist:
     if item['role'] == 'user':
         langchain_history.append(HumanMessage(content=item['content']))
     elif item['role'] =='assistant':
         langchain_history.append(AIMessage(content=item['content']))
    response = chain.invoke({"input":user_input,
         "history": langchain_history} )
    return "", hist+[{'role':"user",'content':user_input},
                     {'role':'assistant','content':response}]
   
def clear_chat():
    return "",[] 

page  = gr.Blocks(
     title = "Inside the Einstein Brain",
     theme = gr.themes.Soft()
)
with page:
     gr.Markdown(
          """
         # Chat with Einstein
         Welcome to your personalized convo with Einstein
          """
     )
     chatbot = gr.Chatbot(avatar_images=[None,'einstein.png'],
      show_label=False
        )
     msg = gr.Textbox(show_label=False,placeholder="Ask the German Scientist anything....")
     msg.submit(chat, [msg,chatbot],[msg,chatbot])
     clear = gr.Button("Clear Chat", variant='secondary')
     clear.click(clear_chat, outputs=[msg,chatbot])


page.launch(share=True)