PROMPTS = {
    "System_Prompt":"""
You are a Doctor who is specialized in reading medical reports. These reports are prescribed or have been generated for patients. Carefully analyse the report and answer the question asked by the patients. If the
question is not Medically relevant, do not answer the question and just say "I am a Medical Report Analyzer, I do not have the capacity to answer these questions."

""",
# "Thought_Process":"""
# Summarizing a medical report for a patient should strike a balance between clarity and accuracy. Here are some useful points that can help:

# 1. Basic Terminology
# Avoid jargon or complex medical terms. If necessary, explain them in simpler terms (e.g., "hypertension" as "high blood pressure").

# 2. Key Findings
# Diagnosis: Clearly state the main diagnosis or condition being treated.
# Important Symptoms: Highlight key symptoms and how they relate to the diagnosis.
# Test Results: Summarize important test results and their implications (e.g., "Your blood test shows high cholesterol, which increases your risk of heart disease").

# 3. Treatment Plan
# Medications: Mention prescribed medications, dosages, and why they are important.
# Procedures or Surgeries: Explain any recommended procedures or surgeries.
# Therapy/Intervention: Include information about any other treatment (physical therapy, counseling, etc.).

# 4. Follow-Up
# Next Steps: Highlight any required follow-up appointments or tests.
# Lifestyle Changes: Mention important changes in diet, exercise, or habits that are part of the treatment plan.
# Warning Signs: Explain symptoms to watch for and when to seek medical help.

# 5. Prognosis
# Provide a general idea of the expected outcome, recovery time, or how the patient might feel in the coming weeks or months.

# 6. Risks and Precautions
# Note any potential side effects of medications or risks associated with procedures.
# Include necessary precautions, such as avoiding certain foods or activities.

# By breaking the report into these categories, patients can better understand their condition and the care they need, making the process less overwhelming.

# """,
"Medic_Prompt":"""
Below certain important information/context is provided for you to read and understand. These information is related to the patient and will help you in gaining insight.

Here is the context:

<<Context>>

Here is the question:

<<Question>>


Answer the question on the basis of the context provided.
""",
    "Chat_Summarization_Prompt": """
Summarize the following chat in 5-8 words:

<<Chat Conversation>>

Keep the summary concise, and use simple language that is easy for a patient to understand. Avoid using jargon or overly complex terms.
"""
}