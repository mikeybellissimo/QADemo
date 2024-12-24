from pydantic import BaseModel, Field
import streamlit as st
import uuid
from typing import Dict, List, TypedDict

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


class Extractor:

    

    class State(BaseModel):
        """Information about users activity within the inspection app."""
        # ^ Doc-string for the entity Person.
        # This doc-string is sent to the LLM as the description of the schema State,
        # and it can help to improve extraction results.

        # Note that:
        # 1. Each field is an `optional` -- this allows the model to decline to extract it!
        # 2. Each field has a `description` -- this description is used by the LLM.
        # Having a good description can help improve extraction results.
        screen: Optional[str] = Field(default=None, description="The screen that the user should be directed to.")
        jobsite: Optional[str] = Field(default=None, description="The jobsite/property/building that the user is located in or interested in.")
        area: Optional[str] = Field(default=None, description="The area/room of the jobsite/property/building that the user is located in or interested in.")

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
        requested_data_prefix = ""
        if st.session_state.next_missing_data == None:
            examples = [
                (
                    "I'm in overmountain inn room 203 and there's a bath with a crack in it",
                    Extractor.State(screen="create_event", jobsite="Overmountain Inn", area="Room 203"),
                ),
                (
                    "Take me home",
                    Extractor.State(screen="create_event"),
                ),
                (
                    "I want to verify some tasks",
                    Extractor.State(screen="create_event"),
                ),
            ]
        # Do all this later when we want to prompt for "What jobsite are you at"
        else:
            examples = [
                (
                    "Requested Data: number_of_floors. \n"
                    "A blue 4 story hotel with 804 rooms",
                    Extractor.Building(number_of_floors=4, number_of_rooms=804),
                ),
                (
                    "Requested Data: number_of_floors. \n"
                    "63",
                    Extractor.Building(number_of_floors=63),
                ),
                (
                    "Requested Data: number_of_rooms. \n"
                    "42",
                    Extractor.Building(number_of_rooms=42),
                ),
            ]

            requested_data_prefix += "Requested Data: " + st.session_state.next_missing_data + ". \n"

        messages = []

        for text, tool_call in examples:
            messages.extend(
                Extractor.tool_example_to_messages({"input": text, "tool_calls": [tool_call]})
            )

        
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert extraction algorithm that extracts information for an application that facilitates building inspections. "
                    "You must figure out what screen of the app the user wishes to go to. "
                    "Select one of the following options: home, create_event, verify_event"
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
            schema=Extractor.State,
            method="function_calling",
            include_raw=False,
        )
        resp =  runnable.invoke({"text": requested_data_prefix + user_input, "examples": messages})
        
       
        
        
        # replace non-empty values in state
        new_values = resp.model_dump()
        for dict_key in new_values:
            
            if new_values[dict_key] != None:
                
                
                st.session_state[dict_key] = new_values[dict_key]


