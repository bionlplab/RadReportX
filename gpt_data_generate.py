import os
import random
import pandas as pd
from openai import AzureOpenAI

from prompts import SEED_EXAMPLES, generation_prompt 


# WITH YOUR OWN SETUP
os.environ["AZURE_OPENAI_KEY"] = ""
os.environ["AZURE_OPENAI_ENDPOINT"] = ""

API_BASE = os.getenv("AZURE_OPENAI_ENDPOINT")
API_KEY = os.getenv("AZURE_OPENAI_KEY")
DEPLOYMENT_NAME = 'got-4o'
API_VERSION = '2024-05-01-preview'

client = AzureOpenAI(
    api_key=API_KEY,
    api_version=API_VERSION,
    base_url=f"{API_BASE}/openai/deployments/{DEPLOYMENT_NAME}"
)


# Function to process a single row and return the results
def process_row(note):
    examples = random.sample(SEED_EXAMPLES, 3)
    prompt = generation_prompt(examples[0], examples[1], examples[2], note)

    generated_disease = ""
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful radiologist."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0,
        )
    except Exception as e:
        print(f"Error generating row {index}: {e}")
            
    raw_output = response.choices[0].message.content.strip()

    generated_disease = raw_output.strip().splitlines()[0]
    start = generated_disease.find('[')
    generated_disease = generated_disease[start:]

    result = {
        "note": note,
        "generated_disease": generated_disease,
        "raw_output": raw_output,
    }
    return result


df = pd.read_csv("./notes.csv")
results = []

for index, row in df.iterrows():
    print(f"Processing row {index}...")
    try:
        result = process_row(row['note'])
        if result is not None:
            results.append(result)
    except Exception as e:
        print(f"Error processing row {index}: {e}")

df_results = pd.DataFrame(results)
df_results.to_csv("gpt_annotated.csv", index=False)
print("Processing complete. Result saved.")