from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from crewai_tools import YoutubeVideoSearchTool, FirecrawlSearchTool
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import requests

from dotenv import load_dotenv

load_dotenv()

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

    @tool("Web search")
    def WebSearchTool(topic: str, **kwargs):
        """
        Search the web for information about a topic using DuckDuckGo API.
        Returns search results with URLs and descriptions.
        """
        try:
            search_url = f"https://api.duckduckgo.com/?q={topic}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(search_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = []
                if 'AbstractURL' in data and data['AbstractURL']:
                    results.append({
                        'title': data.get('Abstract', f'Information about {topic}'),
                        'url': data['AbstractURL'],
                        'snippet': data.get('Abstract', '')
                    })
                if 'RelatedTopics' in data:
                    for topic_item in data['RelatedTopics'][:5]:
                        if isinstance(topic_item, dict) and 'FirstURL' in topic_item:
                            results.append({
                                'title': topic_item.get('Text', f'Related to {topic}'),
                                'url': topic_item['FirstURL'],
                                'snippet': topic_item.get('Text', '')
                            })
                return results
        except Exception as e:
            return f"Web search error: {str(e)}"
        return []


    # ----------------- Agents -----------------
    @agent
    def researcher(self) -> Agent:
        return Agent(
            role="Researcher",
            goal="Deliver accurate insights on {topic} using web sources and YouTube",
            backstory="Experienced researcher synthesizing web & video info",
            tools=[self.WebSearchTool, self.YouTubeSearchTool],
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
                Use the YouTubeSearchTool to find relevant videos and SerperDevTool for web research.
            """,
            expected_output="""
                Structured research summary of {topic}:
                
                ## Overview
                [Provide a concise overview of the topic]
                
                ## Key Findings
                [List main insights and important information]
                
                ## Recommended Websites
                [List specific website URLs with brief descriptions]
                
                ## Recommended YouTube Videos
                [List YouTube video URLs with titles and brief descriptions]
                
                Make sure to include actual URLs and video links in the output.
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
                Preserve all website URLs and YouTube video links from the research task.
            """,
            expected_output="""
                Final summary document on {topic}:
                
                ## Executive Summary
                [Provide a comprehensive but concise summary of the topic]
                
                ## Key Insights
                [Highlight the most important findings and insights]
                
                ## Recommended Resources
                
                ### Websites
                [List and describe recommended websites with full URLs]
                
                ### YouTube Videos
                [List and describe recommended YouTube videos with full URLs]
                
                Ensure all URLs are complete and clickable links.
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
