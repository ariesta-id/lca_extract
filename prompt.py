processes_extract_prompt = """
Based on the following paper, define the LCA-related processes with a main interest in **{main_interest}**.

**Core Instructions:**

1.  **Identify & Separate Processes:** Find all processes related to {main_interest}. If the paper describes steps in different sections (e.g., material preparation, the chemical reaction, the processor machine creation, etc.), create a separate process block for each. **Do not merge or consolidate processes.**

2.  **Use Literal Values (No Calculations):** You **must not** perform any calculations or normalization. Use the exact literal values and units as they appear in the paper for all inputs and outputs.
    -   For each process, set the `output_reference` to match the specific output value mentioned in the source text. For example, if a paper says "producing **50 kg** of H₂ requires **2,750 kWh**," your `output_reference` value for H₂ must be `50`, and the electricity input value must be `2,750`. If there are various scenarios, then each scenario will be a separate process.

3.  **Structure the Data:** Each process must only have three main keys: `output_reference`, `input`, and `output`.
    -   Materials used to build the processor (e.g., steel for a reactor, catalysts) should be listed directly within the `input` section.
    -   End-of-life materials or waste from the processor should be listed in the `output` section.

4.  **Source Everything with Quotes:** For every single item in `input` and `output`, you must provide a source in the `quote` field.
    -   If the source is a sentence, copy-paste it directly.
    -   If the source is a table, the `quote` must clearly state the table number and can include other relevant notes (e.g., `quote: "Table 2. Carbon 1 kg"` or just `quote: "Table 2"`).

5.  **Handle Uncertainty:** If a value is unclear or not stated, add a `note` field to explain the situation.

Before producing the final YAML, think out loud step-by-step, demonstrating that you have carefully read the paper and are following these instructions precisely.
"""

example = r"""
Follow closely this example format including the triple backticks (yaml code block):

```yaml
- process: Artificial Photosynthesys
  output_reference:
    output: carbohydrate
    unit: kg
    value: 1
    is_exact: True
  input:
    sun_ray:
      quote: "The process is driven by light energy absorbed by chlorophyll, which excites electrons to a higher energy state."
      unit: kWh
      value: 400
      is_exact: False
      note: "The value is an approximation"
    carbon_dioxide:
      quote: "Atmospheric carbon dioxide provides the carbon backbone for the synthesis of larger organic molecules."
      unit: kg
      value: 1.47
      is_exact: True
  output:
    carbohydrate:
      quote: "Ultimately, the light-independent reactions yield three-carbon sugar phosphates, which are then converted into carbohydrates."
      unit: kg
      value: 1
      is_exact: True
    oxygen:
      quote: "As a direct result of the photolysis of water molecules, gaseous oxygen is released as a byproduct."
      unit: kg
      value: 1.07
      is_exact: True
- process: Electricity Generation from Natural Gas
  output_reference:
    output: electricity
    unit: MWh
    value: 1
  input:
    natural_gas:
      quote: "Table 4"
      unit: m^3
      value: 172
      is_exact:True
    cooling_water:
      quote: "Table 4"
      unit: kg
      value: 1000
      is_exact: False
  output:
    electricity:
      quote: "Table 4"
      unit: MWh
      value: 1
      is_exact: True
    carbon_dioxide:
      quote: "Table 4"
      unit: kg
      value: 330
      is_exact: True
```
"""
