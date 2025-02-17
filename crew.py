from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool
from dotenv import load_dotenv

from tools.calculator_tool import CalculatorTool
from tools.sec_tools import SEC10KTool, SEC10QTool

load_dotenv()

llm = LLM(model="ollama/deepseek-r1:7b", base_url="http://localhost:11434")


@CrewBase  # type: ignore
class StockAnalysisCrew:
  agents_config = "config/agents.yaml"
  tasks_config = "config/tasks.yaml"

  def __init__(self, inputs=None):
    self.inputs = inputs or {}

  @agent
  def financial_agent(self) -> Agent:
    company_stock = self.inputs.get("company_stock", "AMZN")  # type: ignore
    return Agent(
      config=self.agents_config["financial_analyst"],  # type: ignore
      verbose=True,
      llm=llm,
      tools=[
        ScrapeWebsiteTool(),
        WebsiteSearchTool(),
        CalculatorTool(),
        SEC10QTool(company_stock),
        SEC10KTool(company_stock),
      ],
    )  # type: ignore

  @agent
  def research_analyst_agent(self) -> Agent:
    company_stock = self.inputs.get("company_stock", "AMZN")  # type: ignore
    return Agent(
      config=self.agents_config["research_analyst"],  # type: ignore
      verbose=True,
      llm=llm,
      tools=[
        ScrapeWebsiteTool(),
        SEC10QTool(company_stock),
        SEC10KTool(company_stock),
      ],
    )  # type: ignore

  @task
  def research(self) -> Task:
    return Task(
      config=self.tasks_config["research"],  # type: ignore
      agent=self.research_analyst_agent(),
    )

  @agent
  def financial_analyst_agent(self) -> Agent:
    company_stock = self.inputs.get("company_stock", "AMZN")  # type: ignore
    return Agent(
      config=self.agents_config["financial_analyst"],  # type: ignore
      verbose=True,
      llm=llm,
      tools=[
        ScrapeWebsiteTool(),
        WebsiteSearchTool(),
        CalculatorTool(),
        SEC10QTool(company_stock),
        SEC10KTool(company_stock),
      ],
    )

  @task
  def financial_analysis(self) -> Task:
    return Task(
      config=self.tasks_config["financial_analysis"],  # type: ignore
      agent=self.financial_analyst_agent(),
    )

  @task
  def filings_analysis(self) -> Task:
    return Task(
      config=self.tasks_config["filings_analysis"],  # type: ignore
      agent=self.financial_analyst_agent(),
    )

  @agent
  def investment_advisor_agent(self) -> Agent:
    return Agent(
      config=self.agents_config["investment_advisor"],  # type: ignore
      verbose=True,
      llm=llm,
      tools=[
        ScrapeWebsiteTool(),
        WebsiteSearchTool(),
        CalculatorTool(),
      ],
    )

  @task
  def recommend(self) -> Task:
    return Task(
      config=self.tasks_config["recommend"],  # type: ignore
      agent=self.investment_advisor_agent(),
    )

  @crew
  def crew(self) -> Crew:
    """Creates the Stock Analysis"""
    return Crew(
      agents=self.agents,  # type: ignore
      tasks=self.tasks,  # type: ignore
      process=Process.sequential,
      verbose=True,
    )
