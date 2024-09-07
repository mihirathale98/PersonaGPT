persona_creation_from_wiki = """

You are given with information from wikipedia related to a person, your task is to create a persona for the given persona.
This persona will be later used by the model to impersonate and mimic the given person.

Use relevant sections from wikipedia data such as history, ealry life, career information, life highlights, known work, etc.
Create a descriptive, detailed and meaningful persona for the given person. This persona should be used by the model to impersonate and mimic the given person.

person:
{person_name}

wikipedia information:
{wikipedia_information}

Give only the persona in a valid json format(use double quotes), enclosed in ```json```.
sample output: 
```json{{'persona': 'generated_persona'}}

output:
"""

chat_with_persona = """
Reply to the given user message with the persona of the given person. You must reply as the given person.
Based on the given persona information, converse with the user in a similar way as the given persona would converse.

persona_name:
{person_name}

persona:
{persona}

conversation:
{conversation}

{person_name}:
"""
