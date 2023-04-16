"""The main entry to collect the information from all the sources.
"""
from taotie.consumer.simple_summarizer import SimpleSummarizer
from taotie.gatherer import Gatherer
from taotie.message_queue import SimpleMessageQueue
from taotie.orchestrator import Orchestrator
from taotie.sources.github import GithubTrends
from taotie.sources.http_service import HttpService
from taotie.sources.twitter import TwitterSubscriber


def create_info_printer():
    verbose = True
    batch_size = 1
    fetch_interval = 10
    mq = SimpleMessageQueue()
    instruction = """
    Please summarize the following collected json data in an informative way in Chinese:
    If the json is about a tweets, please refer the id. If it does not contain meaningful information, please ignore it.
    If the json is about a github repos, please summarize them ONE BY ONE and include the repo names and the repo links.
    If the json is a web page, please extract the main content and summarize.
    """
    consumer = SimpleSummarizer(
        buffer_size=1000,
        summarize_instruction=instruction,
        verbose=verbose,
        dedup=True,
        max_tokens=1800,
    )
    gatherer = Gatherer(
        message_queue=mq,
        consumer=consumer,
        batch_size=batch_size,
        fetch_interval=fetch_interval,
        verbose=verbose,
    )

    # Twitter source.
    rules = ["from:RunGreatClasses", "#GPT", "#llm", "#AI", "#AGI", "foundation model"]
    twitter_source = TwitterSubscriber(rules=rules, sink=mq, verbose=verbose)
    # Github source.
    github_source = GithubTrends(sink=mq, verbose=verbose)
    # Http service source.
    http_service_source = HttpService(sink=mq, verbose=verbose, truncate_size=3000)

    orchestrator = Orchestrator()
    orchestrator.set_gatherer(gatherer=gatherer)
    orchestrator.add_source(twitter_source)
    orchestrator.add_source(github_source)
    orchestrator.add_source(http_service_source)
    orchestrator.start()


if __name__ == "__main__":
    create_info_printer()
