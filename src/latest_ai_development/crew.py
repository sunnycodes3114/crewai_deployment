from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tasks.task_output import TaskOutput
# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
@CrewBase
class LatestAiDevelopment():
	"""LatestAiDevelopment crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	def __init__(self, hidden_inputs):
		self.hidden_inputs = hidden_inputs

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	def print_output(self, output: TaskOutput):
		import requests
		# Hasura GraphQL endpoint
		HASURA_GRAPHQL_ENDPOINT = "https://fbjlcpshkpbwfdhhosrh.hasura.ap-south-1.nhost.run/v1/graphql"
		# Admin secret from your Hasura/Nhost console (include the leading colon if shown)
		HASURA_ADMIN_SECRET = ":HK'qiL5cvojcHVzucs-K+tC5H-W@hrH"
		chat_id = self.hidden_inputs["chat_id"]
		bot_message_content = f"{output.agent} says:\n{output.raw}"
		bot_user_id = self.hidden_inputs["bot_user_id"]  # Provided user ID
		mutation = """
		mutation InsertBotMessage($chatId: uuid!, $content: String!, $userId: uuid!) {
		insert_messages_one(object: {
			chat_id: $chatId,
			content: $content,
			is_bot: true,
			user_id: $userId
		}) {
			id
			content
			is_bot
			user_id
			created_at
		}
		}
		"""

		variables = {
			"chatId": chat_id,
			"content": bot_message_content,
			"userId": bot_user_id
		}

		headers = {
			"Content-Type": "application/json",
			"x-hasura-admin-secret": HASURA_ADMIN_SECRET
		}

		response = requests.post(
			HASURA_GRAPHQL_ENDPOINT,
			json={"query": mutation, "variables": variables},
			headers=headers
		)

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			callback=self.print_output
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md',
			callback=self.print_output
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the LatestAiDevelopment crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
