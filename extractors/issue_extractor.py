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
from datetime import datetime, timedelta


class IssueExtractor:
    class Issue(BaseModel):
        """Information about users activity within the inspection app."""
        # ^ Doc-string for the entity Person.
        # This doc-string is sent to the LLM as the description of the schema Issue,
        # and it can help to improve extraction results.

        # Note that:
        # 1. Each field is an `optional` -- this allows the model to decline to extract it!
        # 2. Each field has a `description` -- this description is used by the LLM.
        # Having a good description can help improve extraction results.
        name: Optional[str] = Field(default=None, description="A short, descriptive name/alias for the issue being described.")
        description: Optional[str] = Field(default=None, description="A summary of the raw description provided by the user. It should include all relevant facts and exclude anything unrelated to the issue. It should sound professional.")
        classification: Optional[str] = Field(default=None, description="A classification of the subject of the described issue. The only possible values are: [Entry door, Internal door, Bathroom, Walls, Flooring, Ceiling, Furniture, Appliances, Window]. If the subject of the issue does not fall into one of these categories, assign 'Other'.")
        action_to_resolve: Optional[str] = Field(default=None, description="A classification of the appropriate action required to resolve the described issue. The only possible values are [Fix, Maintain, Replace, Review]. 'Review' should only be chosen if the user indicates it directly or if he appears uncertain to whether it will be an issue or not. If the issue is something that is not able to be resolved by easily fixing or maintaining it, such as a window with extensive glass damage, then it must be replaced.")
        due_datetime: Optional[str] = Field(default=None, description="The datetime the user specifies for when the issue must be resolved, if provided. The datetime should be specified as a string with the following format YYYY-MM-DDTHH:MM.")

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
                    "I'm in overmountain inn room 203 and there's a bath with a fucking big ass crack in it and the water pours out when you turn it on. This needs to be fixed by noon tomorrow.",
                    # The crazy code for setting due_datetime just returns out "noon tomorrow" in the expected format.
                    IssueExtractor.Issue(name="Cracked Bath", description= "The bath has a large crack in it, allowing water to fall through.", classification="Bathroom", action_to_resolve="Replace", due_datetime=datetime.strptime(str(datetime.now() + timedelta(hours=24))[:10] + "T12:00", "%Y-%m-%dT%H:%M").strftime("%Y-%m-%dT%H:%M")),
                ),
                (
                    "There's a massive hole in the ceiling on the south east corner of the room.",
                    IssueExtractor.Issue(name="Hole in Ceiling", description="There is a large hole in the ceiling in the southeast corner of the room.", classification="Ceiling", action_to_resolve="Fix"),
                ),
                (
                    "The couch has a broken leg its the one on the front-left side and now its all slanted. Hold on martha i'm talking give me a second. The dumbass movers must have broken it when they were bringing the damn thing upstairs.",
                    IssueExtractor.Issue(name="Broken Couch Leg", description="The front-left leg of the couch is broken leading to it being slanted. This was likely caused by the movers when transporting it up the stairs.", classification="Furniture", action_to_resolve="Replace"),
                ),
            ]
        # Do all this later when we want to prompt for "What jobsite are you at"
        else:
            examples = [
                (
                    "Requested Data: number_of_floors. \n"
                    "A blue 4 story hotel with 804 rooms",
                    IssueExtractor.Building(number_of_floors=4, number_of_rooms=804),
                ),
                (
                    "Requested Data: number_of_floors. \n"
                    "63",
                    IssueExtractor.Building(number_of_floors=63),
                ),
                (
                    "Requested Data: number_of_rooms. \n"
                    "42",
                    IssueExtractor.Building(number_of_rooms=42),
                ),
            ]

            requested_data_prefix += "Requested Data: " + st.session_state.next_missing_data + ". \n"

        messages = []

        for text, tool_call in examples:
            messages.extend(
                IssueExtractor.tool_example_to_messages({"input": "Current Datetime: " + str(datetime.now().strftime("%Y-%m-%dT%H:%M")) + "\n User Provided Description: " + text, "tool_calls": [tool_call]})
            )

        
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert extraction algorithm that extracts information from a user provided description for an application that facilitates building inspections for the user."
                    # "First, you must come up with a short descriptive name for the issue being described. "
                    # "Next, you must describe the issue in a relevant, professional way. "
                    # "Then, you must classify the issue being described"
                    "Only extract relevant information from the text. "
                    "If you do not know the value of an attribute asked "
                    "to extract, return null for the attribute's value.",
                ),
                # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
                MessagesPlaceholder("examples"),  # <-- EXAMPLES!
                # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
                ("human", "Current Datetime: " + str(datetime.now().strftime("%Y-%m-%dT%H:%M")) + "\n User Provided Description: {text}"),
            ]
        )
        
        openai_api_key = st.secrets["open_ai_api"]

        llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key = openai_api_key)
        
        runnable = prompt | llm.with_structured_output(
            schema=IssueExtractor.Issue,
            method="function_calling",
            include_raw=False,
        )
        resp =  runnable.invoke({"text": requested_data_prefix + user_input, "examples": messages})
        
       
        
        
        # replace non-empty values in state
        new_values = resp.model_dump()
        for dict_key in new_values:
            
            if new_values[dict_key] != None:
                st.session_state.new_issue[dict_key] = new_values[dict_key]


