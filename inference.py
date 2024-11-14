import os
import pandas as pd
import torch
from huggingface_hub import login

from torchtune.models import convert_weights
from torchtune.models.llama3 import llama3_8b, llama3_tokenizer
from torchtune.utils._checkpointing._checkpointer_utils import safe_torch_load
from torchtune import utils

from prompts import prompt_mimic


# USE YOUR OWN TOKEN
login(token="")
device = 'cuda'

print("Loading model and tokenizer...")
model_path = "meta-llama/Meta-Llama-3.1-8B-Instruct"

model = llama3_8b()
model_state_dict = safe_torch_load(
    "meta_model_0.pt"
)
model_state_dict = convert_weights.meta_to_tune(model_state_dict)
model.load_state_dict(model_state_dict)
model.to(device)

tokenizer = llama3_tokenizer("/prj0129/yiw4018/chestxray/fine_tune/Meta-Llama-3-8B-Instruct/original/tokenizer.model")

# Function to process a single row and return the results
def process_row(note):
    prompt_str = prompt_mimic(note)

    tokens = tokenizer.encode(prompt_str, add_bos=True, add_eos=False)
    prompt = torch.tensor(tokens, dtype=torch.int, device=device)

    generated_disease = ""
    ntry = 0
    while (not generated_disease.startswith("[") or not generated_disease.endswith("]")) and ntry < 2:
        try:
            with torch.no_grad():
                outputs = utils.generate(
                    model=model,
                    prompt=prompt,
                    max_generated_tokens=150,
                    temperature=0,
                    stop_tokens=tokenizer.stop_tokens,
                    pad_id=tokenizer.pad_id,
                )

            raw_output = tokenizer.decode(outputs[0])
            disease_start = raw_output.find("Expected Output:")
            if disease_start != -1:
                generated_disease = raw_output[disease_start + len("Expected Output:"):].strip().splitlines()[0]
            ntry += 1
        except Exception as e:
            print(e)

    result = {
        "note": note,
        "generated_disease": generated_disease,
        "raw_output": raw_output,
    }

    print("Generated diseases: " + generated_disease)
    return result

df = pd.read_csv("./data/yishu_radiology_label_100.csv")
print("CSV file read successfully.")

results = []

for index, row in df.iterrows():
    try:
        findings = row['input']
        print(f"Processing row {index}...")
        result = process_row(findings)
        result['study_id'] = row['study_id']
        result['subject_id'] = row['subject_id']
        result['mimic_label'] = row['mimic_label']
        result['negbio_label'] = row['negbio_label']
        result['human_label1'] = row['human_label1']
        result['human_label2'] = row['human_label2']
        results.append(result)
    except Exception as e:
        print(f"Error processing row {index}: {e}")
        print(row['input'])

df_results = pd.DataFrame(results)

df_results.to_csv("mimic_result.csv", index=False)
