persona_creation_from_wiki = """

You are given with information from wikipedia and other sources related to a person, your task is to create a persona for the given persona.
This persona will be later used by the model to impersonate and mimic the given person.

Use relevant sections from wikipedia data such as history, ealry life, career information, life highlights, known work, etc.
You might also find interviews, press statements, and news articles relevant to the given persona and some statements actually said by the given person.
Create a descriptive, detailed and meaningful persona for the given person. This persona should be used by the model to impersonate and mimic the given person.

person:
{person_name}

wikipedia information:
{relevant_information}

Give only the persona in a valid json format(use double quotes), enclosed in ```json```.
sample output: 
```json{{'persona': 'generated_persona'}}

output:
"""

chat_with_persona = """
Reply to the given user message with the persona of the given person. You must reply as the given person.
Based on the given persona information, converse with the user in a similar way as the given persona would converse.

Use the provided extra information if required to answer the users question.

extra information:
{extra_info}

persona_name:
{person_name}

persona:
{persona}

conversation:
{conversation}


{person_name}:
"""


statement_extractor = """
From the following news articles, identify and extract any direct press statements or interview excerpts by {personality}. 
If no direct statements are available, summarize key information related to their public communications, including any relevant press statements or interview highlights.

{news_articles}

Output:"""

statement_extractor_summ = """Summarize the follwing information into a single output,
If there are particular statements extracted in the provided data please do not change them and represent them accordingly, any other information - please summarize accordingly.

Provided Information :
{information}

Output:"""

info_merge_prompt = """
Given the following information, please merge them in a single output without any information redundancy.
the information is regarding a particular person extracted from wikipedia and other sources.
Please do not miss out on any information, especially if there are particular statements extracted in the provided data please do not change them and represent them accordingly, any other information - please summarize accordingly.

wikipedia information:
{wikipedia_information}

other information:
{other_information}

Output:"""
