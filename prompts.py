# first 11 rows from NIH ground truth
# it include impression
# if NO ----, don't include
# the same icd-10 may appear with different phrases
# maybe misspelling: of --> for
# may not be precise match, so actually two-word is better
SEED_EXAMPLES = [
    """
    Report: 'Findings: Swan Ganz catheter is present.  Bilateral pulmonary edema is again seen with areas of bibasilar atelectasis. Enlarged cardiac silhouette is again seen.
            Impression: Stable appearance of bilateral pulmonary edema and bibasilar atelectasis.'
    Output: ['Swan Ganz catheter', 'Bilateral pulmonary edema', 'Bibasilar atelectasis', 'Enlarged cardiac silhouette']
    The reason is: 'Swan Ganz catheter' (Z95.2), 'Bilateral pulmonary edema' (I50.1),  'Bibasilar atelectasis' (J98.11), 'Enlarged cardiac silhouette' (I51.7)
    """,
    """
    Report: 'Findings: Interval placement of right side chest tube. Interval resolution of right pneumothorax. There is a persistent moderate left pleural effusion, improved. No focal consolidation or signs of pulmonary edema. Cardiomediastinal silhouette is stable.
            Impression: Resolution of right-sided pneumothorax. Improving left sided pleural effusion.'
    Output: ['placement of right side chest tube', 'Pleural effusion']
    The reason is: 'placement of right side chest tube' (Z48.02), 'Pleural effusion' (J90)
    """,
    """
    Report: 'Findings: Right chest wall central line with tip terminating in the superior cavoatrial junction. New numerous bilateral pulmonary nodules. No pleural effusion. No pneumothorax. Cardiac silhouette within normal limits.
            Impression: New bilateral pulmonary nodules, differential includes metastatic disease and septic embolic.'
    Output: ['Right chest wall central line with tip terminating in the superior cavoatrial junction', 'numerous bilateral pulmonary nodules', 'Differential includes metastatic disease and septic embolic']
    The reason is: 'Right chest wall central line with tip terminating in the superior cavoatrial junction' (Z45.2), 'Numerous bilateral pulmonary nodules' (J98.4), 'Differential includes metastatic disease and septic embolic' (C79.9)
    """,
    """
    Report: 'Findings: Endotracheal tube with tip terminating in the mid upper thoracic trachea. RIJ line with tip terminating in the distal SVC. Enteric tube with tip terminating within the stomach. Left basilar chest tube in situ. Intact sternotomy wires. 
            Interval enlargement of cardiac silhouette. Increased bilateral pulmonary edema. Small left basilar pneumothorax. Chronic distal right clavicle fracture deformity.
            Impression: Increased size of cardiac silhouette and pulmonary edema suspicious for pericardial effusion with possible tamponade physiology.'
    Output: ['Endotracheal tube in mid upper thoracic trachea', 'RIJ line in distal SVC', 'Enteric tube in stomach', 'Left basilar chest tube in situ', 'Intact sternotomy wires', 'Enlargement of cardiac silhouette', 'Increased bilateral pulmonary edema', 'Small left basilar pneumothorax', 'Chronic distal right clavicle fracture deformity', 'Suspicion of pericardial effusion with possible tamponade physiology']
    The reason is: 'Endotracheal tube in mid upper thoracic trachea' (Z96.1), 'RIJ line in distal SVC' (Z45.2), 'Enteric tube in stomach' (Z43.1), 'Left basilar chest tube in situ' (Z48.02), 'Intact sternotomy wires' (Z95.1), 'Enlargement of cardiac silhouette' (I51.7), 'Increased bilateral pulmonary edema' (I50.1), 'Small left basilar pneumothorax' (J93.9), 'Chronic distal right clavicle fracture deformity' (M84.442A), 'Suspicion of pericardial effusion with possible tamponade physiology' (I31.3)
    """,
    """
    Report: 'Findings: Patchy left lower lung opacity. No effusion. No pneumothorax. Cardiomediastinal silhouette is within normal limits. No acute osseous abnormality. 
            Impression: Patchy left lower lung opacity suspicious for pneumonia. '
    Output: ['Patchy left lower lung opacity']
    The reason is: 'Patchy left lower lung opacity' (J18.9)
    """,
    """
    Report: 'Findings: Interval placement of right chest tube. Decreased, now trace right apical pneumothorax. Unchanged plate-like right midlung atelectasis. Unchanged bibasilar subsegmental atelectasis. Unchanged mild bilateral pulmonary edema. Stable enlarged cardiac silhouette. 
            Impression: Interval placement of right chest tube with decreased, now trace right apical pneumothorax.'
    Output: ['Placement of right chest tube', 'Trace right apical pneumothorax', 'Right midlung atelectasis', 'Bibasilar subsegmental atelectasis', 'Mild bilateral pulmonary edema', 'Enlarged cardiac silhouette']
    The reason is: 'Placement of right chest tube' (Z48.02), 'Trace right apical pneumothorax' (J93.9), 'Right midlung atelectasis' (J98.11), 'Bibasilar subsegmental atelectasis' (J98.11), 'Mild bilateral pulmonary edema' (I50.1), 'Enlarged cardiac silhouette' (I51.7)
    """,
    """
    Report: 'Findings: Moderate left pneumothorax. New large left hilar mass. New bibasilar right greater than left opacities. Unchanged moderate emphysema. 
            Impression: Moderate left pneumothorax. New large right hilar mass suspicious for neoplasm. New bibasilar opacities suspicious for aspiration.'
    Output: ['Moderate left pneumothorax', 'Large left hilar mass', 'Bibasilar opacities', 'Moderate emphysema', 'Large right hilar mass', 'Suspicion of neoplasm', 'Suspicion of aspiration']
    The reason is: 'Moderate left pneumothorax' (J93.11), 'Large left hilar mass' (R22.2), 'Bibasilar opacities' (J84.10), 'Moderate emphysema' (J43.9), 'Large right hilar mass' (R22.1), 'Suspicion of neoplasm' (R22.1), 'Suspicion of aspiration' (J69.0)
    """,
    """
    Report: 'Findings: New left midlung consolidation and right basilar medial consolidation. New layering small left pleural effusion. No right pleural effusion. No right pneumothorax. Unremarkable cardiac silhouette. Stable hyperinflated lungs with coarsened lung markings consistent with emphysema. 
            Impression: Multifocal pneumonia with probable left parapneumonic effusion.'
    Output: ['Midlung consolidation', 'Basilar medial consolidation', 'Small pleural effusion', 'Hyperinflated lungs with coarsened lung markings', 'Multifocal pneumonia', 'Parapneumonic effusion']
    The reason is: 'Midlung consolidation' (J18.9), 'Basilar medial consolidation' (J18.9), 'Small pleural effusion' (J90), 'Hyperinflated lungs with coarsened lung markings' (J43.9), 'Multifocal pneumonia' (J18.2), 'Parapneumonic effusion' (J86.0)
    """,
    """
    Report: 'Findings: Right chest wall dual lumen catheter with tip terminating in the distal SVC. No consolidation. No pleural effusion. No pneumothorax. Unchanged cardiac silhouette. No acute osseous abnormality.
            Impression: No evidence of pneumonia.'
    Output: ['Dual lumen catheter in distal SVC', 'Post-operative fever']
    The reason is: 'Dual lumen catheter in distal SVC' (Z45.2), 'Post-operative fever' (R50.9)
    """,
    """
    Report: 'Findings: Right chest wall central line with tip terminating in the distal SVC.  Unchanged left medially directed pigtail chest tube. Resolved left pneumothorax. New left basilar nodule with  internal air. 
            Impression: New left basilar nodule with internal air suspicious for septic embolism.'
    Output: ['Right chest wall central line', 'Tip terminating in the distal SVC', 'Unchanged left medially directed pigtail chest tube', 'Resolved left pneumothorax', 'New left basilar nodule with internal air', 'Suspicion for septic embolism']
    The reason is: 'Right chest wall central line' (Z45.2), 'Tip terminating in the distal SVC' (T82.817A), 'Unchanged left medially directed pigtail chest tube' (Z46.6), 'Resolved left pneumothorax' (J93.9), 'New left basilar nodule with internal air' (R91.8), 'Suspicion for septic embolism' (I26.99)
    """,
    """
    Report: 'Findings: Right chest wall line with tip terminating in the distal SVC.  No consolidation. New mild peribronchial cuffing. Unremarkable cardiac silhouette. No acute osseous abnormality.  
            Impression: New mild peri-bronchial cuffing representing small airways disease.'
    Output: ['New mild peribronchial cuffing', 'Small airways disease']
    The reason is: 'New mild peribronchial cuffing' (J44.9), 'Small airways disease' (J44.9)
    """,
]


def generation_prompt(example1, example2, example3, note):
    # add 'Include only the conditions that the patient has. For example, if the report states 'No pneumothorax,' do not include pneumothorax.'
    return f"""
    You are a radiologist. Your tasks is to do entity recognition, which will extract phrases in the report that represents a potential ICD-10 code.
    Your result should be a list, i.e. [phrase 1, phrase 2, ...]. The phrase should fully contain the indication of a ICD-10 code, but also should be as short as possible.

    Guidelines:
    * Extract phrases that directly correlate to an ICD-10 code.
    * Keep the phrases as concise as possible while retaining their full meaning.
    * Provide the reasoning behind each extracted phrase, including the corresponding ICD-10 code.
    * Include only the conditions that the patient has. For example, if the report states 'No pneumothorax,' do not include pneumothorax.
    * If there are no conditions or findings that correlate to an ICD-10 code, directly output 'Output: []'

    **Example Reports and Outputs:**

    1. {example1}

    2. {example2}

    3. {example3}

    **Report to Analyze:**
    {note}

    Output:
    """


def prompt_mimic(note):
    return f"""
    You are given a clinical report. Your task is to identify the diseases that the patient have and list them. The result list should be formatted exactly as [disease1, disease2, ...] and be on a single line.

    Only use diseases from this list:
    ['Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema', 'Enlarged Cardiomediastinum', 'Fracture', 'Lung Lesion',
    'Lung Opacity', 'Pleural Effusion', 'Pleural Other', 'Pneumonia', 'Pneumothorax', 'Support Devices']

    Guidelines:
    Be careful about negation. E.g., do not include Pneumonia if the text says "no Pneumonia"
    Only include diseases that are certain. Entities that are 'likely', 'possibly' should not be returned. 
    After output the list, provide the evidence in the text for each disease.    
    
    **Report to Analyze:**
    {note}

    Expected Output:
    """


def get_prompt_icd(note):
    # third example missing item is fixed
    return f"""
    You are a radiologist. Your tasks is to do entity recognition, which will extract phrases in the report that represents a potential ICD-10 code.
    Your result should be a list, i.e. [phrase 1, phrase 2, ...]. The phrase should fully contain the indication of a ICD-10 code, but also should be as short as possible.

    Guidelines:

    Extract phrases that directly correlate to an ICD-10 code.
    Only include facts that are certain. Entities that are 'likely', 'possibly' should not be returned.
    Keep the phrases as concise as possible while retaining their full meaning.
    Provide the reasoning behind each extracted phrase, including the corresponding ICD-10 code.    

    **Example Reports and Outputs:**

    1. Report: 'Swan Ganz catheter is present.  Bilateral pulmonary edema is again seen with areas of bibasilar atelectasis. Enlarged cardiac silhouette is again seen.'
    Output: ['Swan Ganz catheter', 'Bilateral pulmonary edema', 'Bibasilar atelectasis', 'Enlarged cardiac silhouette']
    The reason is: 'Swan Ganz catheter' (Z95.2), 'Bilateral pulmonary edema' (J81.0),  'Bibasilar atelectasis' (J98.11), 'Enlarged cardiac silhouette' (I51.7)

    2. Report: 'Interval placement of right side chest tube. Interval resolution of right pneumothorax. There is a persistent moderate left pleural effusion, improved. No focal consolidation or signs of pulmonary edema. Cardiomediastinal silhouette is stable.'
    Output: ['placement of right side chest tube', 'Pleural effusion']
    The reason is: 'placement of right side chest tube' (Z48.02), 'Pleural effusion' (J90)

    3. Report: 'Right chest wall central line with tip terminating in the superior cavoatrial junction.  New numerous bilateral pulmonary nodules. No pleural effusion. No pneumothorax. Cardiac silhouette within normal limits.'
    Output: ['Right chest wall central line with tip terminating in the superior cavoatrial junction', 'Numerous bilateral pulmonary nodules', 'Differential includes metastatic disease and septic embolic']
    The reason is: 'Right chest wall central line with tip terminating in the superior cavoatrial junction' (Z45.2), 'Numerous bilateral pulmonary nodules' (J98.4), 'Differential includes metastatic disease and septic embolic' (C79.9)

    **Report to Analyze:**
    {note}

    Output:
    """
