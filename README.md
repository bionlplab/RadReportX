# Enhancing disease detection in radiology reports through fine-tuning lightweight LLM on weak labels
This is the code for our work that finetunes a lightweight model (Llama3.1-8B-instruct) from synthetic labels (Arxiv: https://arxiv.org/abs/2409.16563). There are two tasks that this model can achieve. The first task is an open-ended question, which is to detect phrases in a radiology report that represents an ICD-10 code. There is no restriction about the underlying disease. The second task is to detect disease out of 13 candidates from a radiology report. The candidate diseases are [Atelectasis, Cardiomegaly, Consolidation, Edema, Enlarged Cardiomediastinum, Fracture, Lung Lesion, Lung Opacity, Pleural Effusion, Pleural Other, Pneumonia, Pneumothorax, Support Devices]. When there are no diseases out of the candidates, the model will output 'Normal'.

There are two steps to derive the model. The first step is to use GPT4-o or rule based method (Negbio https://arxiv.org/pdf/1712.05898) to generate synthetic labels. The second step is to fine tune the model based on the generated labels.

### Data
mimic_radiologist_label_100.csv: selected MIMIC-CXR reports with human annotated labels

### Model
The base model is Llama3.1-8B-Instruct. The model is uploaded on https://huggingface.co/bionlp/RadReportX.

### GPT data annotation
gpt_data_generate.py 
Leverage GPT4-o to extract entities from radiology reports. Input is csv file containing the notes of interest.

### Fine tune model
The fine tune is based on torchtune framework https://github.com/pytorch/torchtune. Revise the related fields in 8B_lora_single_device.yaml
```
tune run lora_finetune_single_device --config ./8B_lora_single_device.yaml
```

### Inference/Usage
inference.py provides sample usage for inference. It is based on the sample MIMIC-CXR dataset.
The prompts used for inference are listed in prompts.py. The two supported tasks are listed in the introduction section.