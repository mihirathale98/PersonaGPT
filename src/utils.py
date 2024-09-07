import re
import json
import ast

def parse_model_output(model_output):
    matches = re.findall(r"```json(.+?)```", model_output, re.DOTALL)
    if len(matches) == 0:
        return None
    return json.loads(matches[0].strip())
