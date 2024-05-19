from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_structured_chat_agent, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from ImdbTool import ImdbQuery
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

tools = [ImdbQuery()]

# Get the prompt to use - you can modify this!
#prompt = hub.pull("hwchase17/structured-chat-agent")

prompt = ChatPromptTemplate.from_messages(
    messages=[
        SystemMessagePromptTemplate.from_template(
"""
You're an assistant that will help humans by recommending movies/tv series to them.
Respond to the human as helpfully and accurately as possible.
You have access to the following tools:

{tools}

Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or {tool_names}

Provide only ONE action per $JSON_BLOB, as shown:

```

{{

  "action": $TOOL_NAME,

  "action_input": $INPUT

}}

```

Follow this format:

Question: input question to answer

Thought: consider previous and subsequent steps

Action:

```

$JSON_BLOB

```

Observation: action result

... (repeat Thought/Action/Observation N times)

Thought: I know what to respond

Action:

```

{{

  "action": "Final Answer",

  "action_input": "Final response to human"

}}

```

Example of a Final Answer:

```

You: {{
    "action": "Final Answer", 
    
    "action_input": "Based on your preferences, I recommend Movie_Name (Movie_Year). Movie_Synopsis (played by Movie_Actors). It's rated Movie_Rating on IMDb and is classified as Movie_Genres."
}}

```

Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation
"""


# """
# You're an assistant that will help humans by recommending movies/tv series to them. Your goal is to provide helpful and accurate recommendations based on the user's input. Here are the steps to follow:

# 1. **Extract Necessary Information**: Understand the user's preferences and needs from their input to make an accurate search.
# 2. **Provide Detailed Recommendations**: Include additional information about the recommended titles such as synopsis, rating, and genres.

# ### Tools:
# You have access to the following tools:
# - {tools}

# ### Response Format:
# Use a JSON blob to specify a tool by providing an action key (tool name) and an action_input key (tool input). Valid "action" values are "Final Answer" or {tool_names}. Provide only ONE action per JSON blob, as shown:

# ```
# {{
#   "action": $TOOL_NAME,
#   "action_input": $INPUT
# }}
# ```

# ## Observation: action result

#  ... (repeat Thought/Action/Observation N times)

# # Thought: I know what to respond

# ### Example User Query:
# - "I'm looking for a comedy movie with a strong female lead."

# ### Example of a Final Answer:
# ```
# {{
#   "action": "Final Answer",
#   "action_input": "Based on your preferences, I recommend 'The Nice Guys' (2016). This neo-noir action comedy follows two private detectives (played by Ryan Gosling and Russell Crowe) who stumble upon a missing girl case that leads them down a rabbit hole of conspiracy. It features a quirky plot, plenty of action, and a strong female character played by Margaret Qualley. The film is rated R for strong violence and language, but it's still highly enjoyable. It's rated 7.9 on IMDb and is classified as Action, Comedy, and Mystery."
# }}
# ```

# Do not use the information from the examples, utilize them as a template for your answer

# **Important**: Only use information from the tool search for your final answer and don't perform a search if the user hasn't requested a recommendation.
# Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation
# """
),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        HumanMessagePromptTemplate.from_template("{input}\n\n{agent_scratchpad}\n(reminder to respond in a JSON blob no matter what)"),
    ]
)


#llm = Ollama(model="llama3", temperature=0, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
llm = GoogleGenerativeAI(model="models/gemini-pro", temperature=0, google_api_key=os.environ.get("GOOGLE_API_KEY"), callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

agent = create_structured_chat_agent(llm, tools, prompt)

class MovieAgent():
  # Create an agent executor by passing in the agent and tools
  def __init__(self) -> None:
    self.agent_executor = AgentExecutor(
      agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
    )
  
  def run(self, user_input: str):
    return self.agent_executor.invoke({"input": user_input})