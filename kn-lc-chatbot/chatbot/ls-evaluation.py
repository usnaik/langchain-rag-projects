# export LANGSMITH_TRACING=true
# export LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
# export LANGSMITH_API_KEY="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"
# export OPENAI_API_KEY="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"

# 1. Import dependencies
from langsmith import wrappers, Client
from pydantic import BaseModel, Field
from openai import OpenAI

client = Client()
openai_client = wrappers.wrap_openai(OpenAI())

# 2. Create a dataset
# For other dataset creation methods, see: https://docs.smith.langchain.com/evaluation/how_to_guides/manage_datasets_programmatically https://docs.smith.langchain.com/evaluation/how_to_guides/manage_datasets_in_application
# Create inputs and reference outputs
examples = [
  (
      "Which country is Mount Kilimanjaro located in?",
      "Mount Kilimanjaro is located in Tanzania.",
  ),
  (
      "What is Earth's lowest point?",
      "Earth's lowest point is The Dead Sea.",
  ),
]

inputs = [{"question": input_prompt} for input_prompt, _ in examples]
outputs = [{"answer": output_answer} for _, output_answer in examples]

# Programmatically create a dataset in LangSmith
dataset = client.create_dataset(
	dataset_name = "Sample dataset",
	description = "A sample dataset in LangSmith."
)

# Add examples to the dataset
client.create_examples(inputs=inputs, outputs=outputs, dataset_id=dataset.id)

# 3. Define what you're evaluating
# Define the application logic you want to evaluate inside a target function
# The SDK will automatically send the inputs from the dataset to your target function
def target(inputs: dict) -> dict:
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            { "role": "system", "content": "Answer the following question accurately" },
            { "role": "user", "content": inputs["question"] },
        ]
    )
    return { "response": response.choices[0].message.content.strip() }

# 4. Define evaluator
# Define instructions for the LLM judge evaluator
instructions = """Evaluate Student Answer against Ground Truth for conceptual similarity and classify true or false: 
- False: No conceptual match and similarity
- True: Most or full conceptual match and similarity
- Key criteria: Concept should match, not exact wording.
"""

# Define output schema for the LLM judge
class Grade(BaseModel):
    score: bool = Field(description="Boolean that indicates whether the response is accurate relative to the reference answer")

# Define LLM judge that grades the accuracy of the response relative to reference output
def accuracy(outputs: dict, reference_outputs: dict) -> bool:
  response = openai_client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
      { "role": "system", "content": instructions },
      { "role": "user", "content": f"""Ground Truth answer: {reference_outputs["answer"]}; 
      Student's Answer: {outputs["response"]}"""
  }],
    response_format=Grade
  );
  return response.choices[0].message.parsed.score

# 5. Run and view results
# After running the evaluation, a link will be provided to view the results in langsmith
experiment_results = client.evaluate(
    target,
    data = "Sample dataset",
    evaluators = [
        accuracy,
        # can add multiple evaluators here
    ],
    experiment_prefix = "first-eval-in-langsmith",
    max_concurrency = 2,
)