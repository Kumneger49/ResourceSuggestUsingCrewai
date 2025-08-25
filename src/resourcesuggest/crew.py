from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from crewai_tools import YoutubeVideoSearchTool, FirecrawlSearchTool, SerperDevTool
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from youtubesearchpython import VideosSearch

@CrewBase
class ResourceSuggester:

    agents: List[BaseAgent]
    tasks: List[Task]

    @tool("Youtube scraper")
    def YouTubeSearchTool(topic: str, **kwargs):
        """
        Custom tool that takes a topic and returns five main videos for that topic.
        Returns a list of dictionaries containing video title and link.
        """
        # use the actual topic passed to the tool
        videos = VideosSearch(topic, limit=5, **kwargs)
        
        videoList = []
        for v in videos.result()['result']:
            videoList.append({"title": v['title'], "link": v['link']})
        
        return videoList


    # ----------------- Agents -----------------
    @agent
    def researcher(self) -> Agent:
        return Agent(
            role="Researcher",
            goal="Deliver accurate insights on {topic} using web sources and YouTube",
            backstory="Experienced researcher synthesizing web & video info",
            tools=[SerperDevTool(), self.YouTubeSearchTool],
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            role="Writer",
            goal="Create clear, engaging summaries of research findings",
            backstory="Skilled content writer producing concise summaries",
            verbose=True
        )

    # ----------------- Tasks -----------------
    @task
    def research_task(self) -> Task:
        return Task(
            name="research_task",
            agent=self.researcher(),
            description="""
                Research {topic} thoroughly using reliable web sources and YouTube.
                Summarize main ideas, identify high-quality websites, and find relevant YouTube videos.
            """,
            expected_output="""
                Structured research summary of {topic}:
                - Concise overview
                - List of website URLs
                - List of YouTube video links
            """
        )

    @task
    def summary_task(self) -> Task:
        return Task(
            name="summary_task",
            agent=self.writer(),
            description="""
                Create a polished summary of research findings on {topic}.
                Highlight important insights, be concise, and reference URLs and videos.
            """,
            expected_output="""
                Final summary document on {topic}:
                - Main ideas explained
                - Key resources highlighted
                - List of recommended websites and YouTube videos
            """,
            context=[self.research_task()],  # link to research_task
            output_file="output/summary.md"
        )

    # ----------------- Crew -----------------
    @crew
    def crew(self) -> Crew:
        return Crew(
            tasks=[self.research_task(), self.summary_task()],
            agents=[self.researcher(), self.writer()],
            process=Process.sequential,
            verbose=True
        )
