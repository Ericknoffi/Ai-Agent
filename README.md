# Agent

## Overview

This repository contains a small agent framework with gateway, nodes, and tools. It provides a starting structure for building modular agent components.

## Project structure

- `main.py` - entry point
- `config.py` - configuration
- `registry.py` - component registry
- `Gateway/` - gateway implementation and models
- `Nodes/` - agent nodes (Planner, Researcher, Coder, Finalizer, etc.)
- `Tools/` - utility tools (Filesystem, Web, Github, Documentation)

## Quick start

1. Create and activate a virtual environment:

   Windows:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   cmd:

   ```cmd
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Create a `.env` file for secrets or keys used by the project.

4. Run the agent:

   ```bash
   python main.py
   ```

## Notes

- Update `requirements.txt` with additional packages your nodes or tools require.
- The generated `.gitignore` includes common Python and editor ignores.
