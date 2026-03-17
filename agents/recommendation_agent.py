"""
Recommendation Agent
Translates insights into concrete, prioritized business strategies.
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


class RecommendationAgent:
    def __init__(self, llm: ChatOpenAI = None):
        if llm is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0.4, api_key=api_key)
        else:
            self.llm = llm

    def generate_recommendations(self, insights: str, context: dict = None) -> str:
        prompt = f"""
        Based on these e-commerce insights, generate 3-5 actionable business recommendations.
        Each recommendation should:
        - Be specific and measurable
        - Include an expected impact
        - Have a priority level (High/Medium/Low)
        
        Insights:
        {insights}
        
        Additional Context: {context or 'None'}
        
        Format each as: [PRIORITY] Action → Expected Impact
        """
        messages = [SystemMessage(content="You are a senior e-commerce growth strategist."),
                    HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)
        return response.content
