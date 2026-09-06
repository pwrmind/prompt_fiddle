# 🎻 Prompt Fiddle

Prompt Fiddle is a lightweight, terminal-based prompt engineering playground designed for local LLMs (powered by Ollama) and OpenAI-compatible APIs. It treats prompts as code, allowing you to fine-tune system instructions and generation parameters with absolute reproducibility, while tracking changes using a beautiful, color-coded terminal diff.
Inspired by the concept of JSFiddle, Prompt Fiddle provides a clean, isolated environment to experiment, iterate, and scientifically test your prompts directly from your favorite terminal.
------------------------------

## ✨ Features

* Prompt-as-Code Architecture: Keep your orchestration logic (config.yaml) completely separate from your raw data inputs (input.txt).
* Live Color-Coded Diff: Automatically compares the latest model response with the previous one. Instantly see what words the model added (+) or removed (-) when you tweak your instructions.
* Maximum Determinism: Out-of-the-box configuration profiles tailored to suppress LLM randomness (temperature: 0.0, top_k: 1, fixed seed), ensuring token-to-token reproducibility.
* Ollama & Cloud Agnostic: Seamlessly switch between local models (like DeepSeek-R1, Llama 3, SmolLM2) and cloud APIs by changing a single line in your config.
* Zero-Install Execution: Powered by uv, allowing anyone to run your project instantly without messy virtual environment setups.

------------------------------
## 🚀 Quick Start (No Installation Needed)
If you have uv installed, you don't even need to clone this repository to try it out. You can run Prompt Fiddle directly via URL:

uv run --with pyyaml --with requests --with colorama https://githubusercontent.com

## Local Setup for Development

   1. Clone the repository:
   
   git clone https://github.com
   cd prompt-fiddle
   
   2. Prepare your workspace:
   Create a config.yaml and an input.txt file in the root directory (see templates below).
   3. Run Prompt Fiddle:
   uv will automatically isolate the environment, resolve dependencies, and boot the script instantly:
   
   uv run main.py
   
   
------------------------------
## ⚙️ Configuration Setup## 1. config.yaml
This file holds your engine parameters. To achieve maximum reproducibility during testing, use the following low-level settings:

```
# Target model pulled via Ollama (e.g., smollm2:latest, deepseek-r1:8b, llama3.1)model: "smollm2:latest"api_base: "http://localhost:11434"
# Global behavior instructions for the modelsystem_prompt: "STAGE 0: Decompose the TASK into STAGES and STEPS. Output results strictly using Markdown."
# Advanced generation settings (Fine-tuned for greedy deterministic search)options:
  temperature: 0.0          # Completely suppress randomness
  seed: 42                  # Fix token generation patterns
  top_k: 1                  # Choose strictly the single most probable token at each step
  top_p: 1.0
  num_ctx: 4096             # Context window size
  repeat_penalty: 1.0       # Disable penalties to observe raw structural behavior
```

## 2. input.txt
Paste your raw data, logs, or tasks directly here. This file is fed straight into the user prompt channel:

TASK
Create telegram bot in python

------------------------------
## 📊 How It Works: The Prompt Science Workflow
When you run uv run main.py, Prompt Fiddle executes the following cycle:

   1. It parses your config.yaml and merges missing flags with safe defaults.
   2. It fetches the raw text block from input.txt.
   3. It dispatches a low-level payload to your local Ollama instance.
   4. It streams the response live in your terminal.
   5. The Magic: It reads .prompt_cache.txt, calculates a granular text difference using difflib, and prints a beautiful map of modifications:

📊 PREVIOUS RESPONSE COMPARISON:+ Added  - Removed--------------------------------------------------
  STAGE 1: Define the Telegram Bot
  STEPS:- 1.1. Select a generic python web framework (e.g. Flask).+ 1.1. Choose a specialized library to use for creating the Telegram Bot (e.g. aiogram).

------------------------------
## 📂 Project Structure

prompt-fiddle/
├── .gitignore             # Keeps caches and .venv out of your commits
├── .prompt_cache.txt      # Automated cache storing the last LLM response
├── config.yaml            # Model configuration & system instructions
├── input.txt              # Raw user payload input
├── main.py                # Core Python application logic (PEP 723 metadata included)
└── README.md              # Documentation

------------------------------
## 🤝 Contributing
Prompt Fiddle is completely open-source. Feel free to open issues or submit pull requests if you want to add capabilities like prompt version history logging, generation time/token counters, or multi-model A/B split testing.
License: MIT

