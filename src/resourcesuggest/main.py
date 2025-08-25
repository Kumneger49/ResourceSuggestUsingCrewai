# main.py
from resourcesuggest.crew import ResourceSuggester

def run():
    topic = input("What topic do you want to research? ")
    crew = ResourceSuggester().crew()
    result = crew.kickoff(inputs={"topic": topic})
    print("Crew has finished the task!")
    print("Result:", result)

# Optional: allow direct script execution
if __name__ == "__main__":
    run()
