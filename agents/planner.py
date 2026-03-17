"""
Planner Agent
Decomposes user queries into ordered execution plans for downstream agents.
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


class PlannerAgent:
    def __init__(self, llm: ChatOpenAI = None):
        if llm is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)
        else:
            self.llm = llm
        self.system_prompt = """
        You are a planning agent for an e-commerce analytics system.
        Given a user query and dataset schema, break the task into clear analysis steps.
        Return a JSON list of steps, each with: step_id, agent, task, priority.
        Agents available: data_agent, insight_agent, recommendation_agent.
        """

    def create_plan(self, query: str, schema: dict) -> dict:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Query: {query}\nSchema: {schema}")
        ]
        response = self.llm.invoke(messages)
        return {"plan": response.content, "query": query}
