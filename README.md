# Introduction
This skill allows you to refine your prompts before providing them to your Roblox coding agents. Assuming you already have coding agents set up with instructions and an environment connected to the Roblox Studio MCP, this skill does not directly create or modify games; rather, it helps you better guide your agents.

# Use Case
This skill is designed to help your agents replicate visual elements based on references. It is not intended for raw coding logic (databases, game mechanics, server-side logic, etc.).

# How to Use
First, specify whether your agent has vision capabilities (image-text-to-text) or not (text-to-text)—for example: "My coding agent has vision." Next, attach your reference materials, add the instruction "improve this prompt using the roblox-prompt-engineer skill," and describe what you would like to achieve. The agent will then provide a refined prompt for you to copy.

# Installation
## Harness (CLI/Local Environment)
- Manual method:
Clone this repository, remove the "README.md" file, and place the contents into your agent's "skills" directory (e.g., `.claude/skills` or `.agents/skills`).
- Automatic method:
Ask your agent directly to install it by providing the link to this GitHub repository.
## Browser-based
If you are using the model via a web browser, download this repository locally, remove the "README" file, and look for an "import skill" or "add custom skill" option. You can also ask the model if it can install a skill directly from a public GitHub repository; if so, simply provide it with the link to this repository.

# Second iteration
The coding agents will send you screenshots, or you can simply explore the project yourself within Roblox Studio. If the results meet your expectations, you can stop there. Otherwise, send the screenshots to your Roblox prompt engineer, explain what isn't working, and they will provide you with a corrective prompt.