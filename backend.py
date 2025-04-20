from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_community.tools import SerperDevTool
from langchain.tools import Tool
from newspaper import Article
from urllib.parse import urlparse
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Newspaper3k tool for fetching article text
def fetch_article(url):
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return f"Invalid URL format: {url}"
        article = Article(url, timeout=10)
        article.download()
        article.parse()
        content = article.text
        # Limit content size for faster processing
        return content[:2500] if content and len(content) > 50 else f"Insufficient content from {url}"
    except Exception as e:
        logger.error(f"Error fetching article from {url}: {str(e)}")
        return f"Error fetching content from {url}: {str(e)}"

fetch_tool = Tool(
    name="FetchArticle",
    func=fetch_article,
    description="Fetch article text from URLs with robust error handling."
)

def generate_article(topic, model, article_length, num_sources, article_style, target_audience, progress_callback=None):
    """
    Generate an article using the CrewAI framework.
    
    Args:
        topic (str): The article topic
        model (str): The OpenAI model to use
        article_length (int): Approximate word count for the article
        num_sources (int): Number of sources to include
        article_style (str): Style of the article 
        target_audience (str): Target audience for the article
        progress_callback (function): Callback function to update progress in the UI
    
    Returns:
        tuple: (research_text, analysis_text, article_text)
    """
    try:
        # Initialize the LLM
        llm = ChatOpenAI(
            model=model,
            temperature=0.7
        )
        
        # Initialize the Serper tool
        search_tool = SerperDevTool()
        
        # Create the journalist agent
        journalist_agent = Agent(
            role="AI Journalist",
            goal=f"Create a {article_style.lower()} article for {target_audience if target_audience else 'a general audience'}",
            tools=[search_tool, fetch_tool],
            llm=llm,
            backstory="A versatile journalist who creates quality articles adapted to different audiences and styles.",
            verbose=True
        )
        
        # Step 1: Research
        if progress_callback:
            progress_callback("Research", "Searching for relevant sources...", 15)
            
        research_task = Task(
            description=f"Find {num_sources} relevant and authoritative URLs on '{topic}'. Format as numbered markdown links.",
            agent=journalist_agent,
            expected_output=f"{num_sources} markdown-formatted URLs"
        )
        
        # Execute research task
        crew_research = Crew(
            agents=[journalist_agent],
            tasks=[research_task],
            verbose=True,
            process=Process.sequential
        )
        research_result = crew_research.kickoff()
        
        # Process research results
        if hasattr(research_result, 'raw'):
            research_text = str(research_result.raw)
        else:
            research_text = str(research_result)
            
        if progress_callback:
            progress_callback("Research", "Found relevant sources!", 30)
        
        # Step 2: Analysis
        if progress_callback:
            progress_callback("Analysis", "Analyzing content from sources...", 45)
            
        analysis_task = Task(
            description=f"Fetch and analyze the content from each URL related to '{topic}'. Summarize each source in 2-3 sentences.",
            agent=journalist_agent,
            context=[research_task],
            expected_output="Concise summaries of each source's key points"
        )
        
        # Execute analysis task
        crew_analysis = Crew(
            agents=[journalist_agent],
            tasks=[analysis_task],
            verbose=True,
            process=Process.sequential
        )
        analysis_result = crew_analysis.kickoff()
        
        # Process analysis results
        if hasattr(analysis_result, 'raw'):
            analysis_text = str(analysis_result.raw)
        else:
            analysis_text = str(analysis_result)
            
        if progress_callback:
            progress_callback("Analysis", "Source analysis complete!", 60)
        
        # Step 3: Writing
        if progress_callback:
            progress_callback("Writing", "Crafting your article...", 75)
            
        writing_task = Task(
            description=f"""
            Write a {article_style.lower()} article about '{topic}' that is approximately {article_length} words. 
            Target audience: {target_audience if target_audience else 'general readers'}.
            Format with markdown: include a compelling headline, introduction, main content sections with subheadings, and a conclusion.
            Base your article on the research and analysis results provided.
            """,
            agent=journalist_agent,
            context=[research_task, analysis_task],
            expected_output="A well-structured markdown article"
        )
        
        # Execute writing task
        crew_writing = Crew(
            agents=[journalist_agent],
            tasks=[writing_task],
            verbose=True,
            process=Process.sequential
        )
        writing_result = crew_writing.kickoff()
        
        # Process final article
        if hasattr(writing_result, 'raw'):
            article_text = str(writing_result.raw)
        else:
            article_text = str(writing_result)
            
        if progress_callback:
            progress_callback("Complete", "Article generation completed successfully!", 100)
        
        return research_text, analysis_text, article_text
        
    except Exception as e:
        logger.error(f"Error generating article: {str(e)}")
        raise e