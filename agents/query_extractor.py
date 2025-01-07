from pydantic import BaseModel, Field
import streamlit as st
import uuid
from typing import Dict, List, TypedDict
from datetime import datetime, timedelta
from typing import Optional
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI


class QueryExtractor:

    

    class Query(BaseModel):
        """Information about the SQLite query that will display the desired information from the 'issue' table to the user of the inspection application."""
        # ^ Doc-string for the entity Query.
        # This doc-string is sent to the LLM as the description of the schema Query,
        # and it can help to improve extraction results.

        # Note that:
        # 1. Each field is an `optional` -- this allows the model to decline to extract it!
        # 2. Each field has a `description` -- this description is used by the LLM.
        # Having a good description can help improve extraction results.

        # We need a vector search to get the description and name searchable properly
        select_query: Optional[str] = Field(default=None, description="The SELECT query that the application will use to display the requested information.") 

        
    class Example(TypedDict):
        """A representation of an example consisting of text input and expected tool calls.

        For extraction, the tool calls are represented as instances of pydantic model.
        """
        
        input: str  # This is the example text
        tool_calls: List[BaseModel]  # Instances of pydantic model that should be extracted


    def tool_example_to_messages(example: Example) -> List[BaseMessage]:
        """Convert an example into a list of messages that can be fed into an LLM.

        This code is an adapter that converts our example to a list of messages
        that can be fed into a chat model.

        The list of messages per example corresponds to:

        1) HumanMessage: contains the content from which content should be extracted.
        2) AIMessage: contains the extracted information from the model
        3) ToolMessage: contains confirmation to the model that the model requested a tool correctly.

        The ToolMessage is required because some of the chat models are hyper-optimized for agents
        rather than for an extraction use case.
        """
        messages: List[BaseMessage] = [HumanMessage(content=example["input"])]
        tool_calls = []
        for tool_call in example["tool_calls"]:
            tool_calls.append(
                {
                    "id": str(uuid.uuid4()),
                    "args": tool_call.model_dump(),
                    # The name of the function right now corresponds
                    # to the name of the pydantic model
                    # This is implicit in the API right now,
                    # and will be improved over time.
                    "name": tool_call.__class__.__name__,
                },
            )
        messages.append(AIMessage(content="", tool_calls=tool_calls))
        tool_outputs = example.get("tool_outputs") or [
            "You have correctly called this tool."
        ] * len(tool_calls)
        for output, tool_call in zip(tool_outputs, tool_calls):
            messages.append(ToolMessage(content=output, tool_call_id=tool_call["id"]))
        return messages
    
    def find_next_missing_data(state_data):
        for i in state_data:
            if state_data[i] == None:
                return i
        else:
            return None

    def extract(user_input):
        
        examples = [
            (
                "Show me all plumbing tasks in the Overmountain Inn",
                QueryExtractor.Query(select_query="SELECT * FROM issue WHERE classification='Bathroom' AND jobsite='Overmountain Inn'"),
            ),
            (
                "All tasks",
                QueryExtractor.Query(select_query="SELECT * FROM issue"),
            ),
            (
                "Show me the tasks due by next week",
                QueryExtractor.Query(select_query="SELECT * FROM issue WHERE due_datetime<" + datetime.strptime(str(datetime.now() + timedelta(days=7))[:10] + "T12:00", "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d") + ";"),
            ),
        ]
        
        messages = []

        for text, tool_call in examples:
            messages.extend(
                QueryExtractor.tool_example_to_messages({"input": text, "tool_calls": [tool_call]})
            )

        
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert SQL query writing algorithm that writes SELECT statements for an application that helps with people who perform building inspections. "
                    "The available fields in the table are ['name', 'description', 'classification', 'action_to_resolve', 'due_datetime', 'jobsite', 'area']. \n"
                    "The 'classification' field can only be one of the following values: [Entry door, Internal door, Bathroom, Walls, Flooring, Ceiling, Furniture, Appliances, Window]. "
                    "The 'action_to_resolve' field can only be one of the following values: [Fix, Maintain, Replace, Review]"
                    "NEVER output any data/schema modification queries so it should never try to drop, update, insert, alter, commit, etc. "
                    "Only extract relevant information from the text. "
                    "If you do not know the value of an attribute asked "
                    "to extract, return null for the attribute's value.",
                ),
                # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
                MessagesPlaceholder("examples"),  # <-- EXAMPLES!
                # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
                ("human", "{text}"),
            ]
        )
        
        openai_api_key = st.secrets["open_ai_api"]

        llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key = openai_api_key)
        
        runnable = prompt | llm.with_structured_output(
            schema=QueryExtractor.Query,
            method="function_calling",
            include_raw=False,
        )
        resp =  runnable.invoke({"text": user_input, "examples": messages})
        
        
        
        # replace non-empty values in state
        new_values = resp.model_dump()
        for dict_key in new_values:
            
            if new_values[dict_key] != None:
                st.session_state.query[dict_key] = new_values[dict_key]


