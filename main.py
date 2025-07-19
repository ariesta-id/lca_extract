# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "replicate",
# ]
# ///
import datetime
import re

import replicate

import prompt


def read_md(file_path):
    with open(file_path, "r") as f:
        return f.read()


### --- Paper input and model option -------------------------------------- ###
PAPER = read_md("lca_pv.md")
MAIN_INTEREST = "photovoltaic life cycle assessment"

GPT_4_1_ID = "openai/gpt-4.1"
O1_ID = "openai/o1"
CLAUDE_4_SONNET_ID = "anthropic/claude-4-sonnet"

MODEL_CHOICE = O1_ID
### ----------------------------------------------------------------------- ###

model_name = MODEL_CHOICE.split("/")[-1]
print(f"Using model: {model_name}")

TEMPERATURE = 0
MAX_OUTPUT_TOKENS = 32 * 1024

gpt_4_1_input = {
    "temperature": TEMPERATURE,
    "max_completion_tokens": MAX_OUTPUT_TOKENS,
}

o1_input = {
    # o1 doesn't accept temperature, weird
    "max_completion_tokens": MAX_OUTPUT_TOKENS,
    "reasoning_effort": "high",
}

claude_4_sonnet_input = {
    "temperature": TEMPERATURE,
    "max_tokens": MAX_OUTPUT_TOKENS,
    "thinking_budget_tokens": 32 * 1024,
    "extended_thinking": True,
}


if MODEL_CHOICE == CLAUDE_4_SONNET_ID:
    model_input = claude_4_sonnet_input
elif MODEL_CHOICE == GPT_4_1_ID:
    model_input = gpt_4_1_input
elif MODEL_CHOICE == O1_ID:
    model_input = o1_input
else:
    raise ValueError("Unknown model")

model_input["system_prompt"] = (
    prompt.processes_extract_prompt.format(main_interest=MAIN_INTEREST)
    + prompt.example
    + "\n"
)
model_input["prompt"] = PAPER

output = replicate.run(MODEL_CHOICE, input=model_input)

text_output = "".join(output)

# Save with timestamp
now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d%H%M%S")
with open(f"{model_name}_output_{timestamp}.txt", "w") as f:
    f.write(text_output)

# Extract the yaml, enclosed by "```yaml" and "```".
# If there are multiple blocks, save as different files per yaml block
yaml_blocks = re.findall(r"```yaml(.*?)```", text_output, re.DOTALL)
print(f"YAML blocks found: {len(yaml_blocks)} blocks")
for i, yaml_block in enumerate(yaml_blocks):
    yaml_block = yaml_block.strip()
    print(f"Block #{i + 1}")
    print(yaml_block)
    print()
    with open(f"{model_name}_output_{timestamp}_{i}.yaml", "w") as f:
        f.write(yaml_block)
