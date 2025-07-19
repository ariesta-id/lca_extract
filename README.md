# Usage

Install [`uv` (link)](https://docs.astral.sh/uv/getting-started/installation/)

Create [replicate.com](https://replicate.com/) account, have some credits, and generate an API key from there.

```bash
export REPLICATE_API_TOKEN=r8_2Bg**********************************
```

Edit this part in `main.py`:

```python
### --- Paper input and model option -------------------------------------- ###
PAPER = read_md("lca_pv.md")
MAIN_INTEREST = "photovoltaic life cycle assessment"

GPT_4_1_ID = "openai/gpt-4.1"
O1_ID = "openai/o1"
CLAUDE_4_SONNET_ID = "anthropic/claude-4-sonnet"

MODEL_CHOICE = O1_ID
### ----------------------------------------------------------------------- ###
```

Edit the paper markdown filepath, the "main interest" of the LCA, and your replicate model.

To run the code, use `uv`

```bash
uv run main.py
```

Code will generate at least one file, `txt`, that is the LLM's response. For each `yaml` code block inside the response, a `yaml` will be created. See the output samples in folder `output_samples`.

# Paper markdown conversion

I used [docling](https://docling-project.github.io/docling/) to convert from PDF to markdown. I also used [Obsidian Web Clipper](https://obsidian.md/clipper) for online paper conversion to markdown. 