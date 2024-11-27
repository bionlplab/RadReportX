# Enhancing disease detection in radiology reports through fine-tuning lightweight LLM on weak labels

## Purpose

Despite significant progress in applying large language models (LLMs) to the medical domain, several limitations still prevent them from practical applications. Among these are the constraints on model size and the lack of cohort-specific labeled datasets. In this work, we investigated the potential of improving a lightweight LLM, such as Llama 3.1-8B, through fine-tuning with datasets using synthetic labels. 

This is the code for our work that finetunes a lightweight model (Llama3.1-8B-instruct) from synthetic labels. This model can achieve two tasks. The first task is an open-ended question, which is to detect phrases in a radiology report that represent an ICD-10 code. There is no restriction on the underlying disease. The second task is to detect diseases out of 13 candidates from a radiology report. The candidate diseases are [*Atelectasis, Cardiomegaly, Consolidation, Edema, Enlarged Cardiomediastinum, Fracture, Lung Lesion, Lung Opacity, Pleural Effusion, Pleural Other, Pneumonia, Pneumothorax, Support Devices*]. When there are no diseases out of the candidates, the model will output 'Normal'.

There are two steps to derive the model. The first step is to use the GPT-4o or rule-based method ([Negbio](https://arxiv.org/pdf/1712.05898)) to generate synthetic labels. The second step is to fine-tune the model based on the generated labels.

## Usage

### Data

`mimic_radiologist_label_100.csv`: selected MIMIC-CXR reports with human annotated labels

### Model

The base model is Llama3.1-8B-Instruct. The model is uploaded on https://huggingface.co/bionlp/RadReportX.

### GPT data annotation

`gpt_data_generate.py`: Leverage GPT4-o to extract entities from radiology reports. Input is csv file containing the notes of interest.

### Fine tune model

The fine tuning is based on [torchtune framework](https://github.com/pytorch/torchtune). Revise the related fields in 8B_lora_single_device.yaml

```
tune run lora_finetune_single_device --config ./8B_lora_single_device.yaml
```

### Inference/Usage
inference.py provides sample usage for inference. It is based on the sample MIMIC-CXR dataset.
The prompts used for inference are listed in prompts.py. The two supported tasks are listed in the introduction section.

## Reference

This repository contains source codes for the work introduced in the following paper:

```
Wei Y, Wang X, Ong H, Zhou Y, Flanders A, Shih G, Peng Y.
Enhancing disease detection in radiology reports through fine-tuning lightweight LLM on weak labels.
arXiv preprint arXiv:2409.16563. 2024 Sep 25.
```


## Acknowledgment

This work was supported by the National Science Foundation Faculty Early Career Development (CAREER) award number
2145640, the Intramural Research Program of the National Institutes of Health, and the Amazon Research Award. The Medical Imaging and Data Resource Center (MIDRC) is funded by the National Institute of Biomedical Imaging and Bioengineering (NIBIB) of the National Institutes of Health under contract 75N92020D00021 and through The Advanced Research Projects Agency for Health (ARPA-H).
