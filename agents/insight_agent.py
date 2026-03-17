"""
Insight Agent
Uses LLM to convert analysis results into human-readable insights.
Includes a reflection loop for self-validation.
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import json


class InsightAgent:
    def __init__(self, llm: ChatOpenAI = None):
        if llm is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0.3, api_key=api_key)
        else:
            self.llm = llm

    def generate_insights(self, analysis_results: dict) -> str:
        prompt = f"""
        You are a senior e-commerce data analyst. Based on the following analysis results,
        generate clear, concise business insights. Be specific with numbers.
        
        Analysis Results:
        {json.dumps(analysis_results, indent=2)}
        
        Format: 3-5 bullet points, each starting with a key metric or finding.
        """
        messages = [SystemMessage(content="You are a data-driven business analyst."),
                    HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)
        return self._reflect(response.content, analysis_results)

    def _reflect(self, insights: str, data: dict) -> str:
        """Self-critique: verify insights are grounded in data."""
        critique_prompt = f"""
        Review these insights and confirm each is supported by the data.
        If any claim is unsupported, remove or correct it.
        
        Insights: {insights}
        Data: {json.dumps(data, indent=2)}
        
        Return only the verified, corrected insights.
        """
        messages = [SystemMessage(content="You are a fact-checker for analytics reports."),
                    HumanMessage(content=critique_prompt)]
        response = self.llm.invoke(messages)
        return response.content
