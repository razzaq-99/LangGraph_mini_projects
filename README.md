# LangGraph Mini Projects

A hands‑on collection of **LangGraph** mini projects (from basics to advanced) built in **Jupyter Notebooks**. Each notebook demonstrates a focused pattern—stateful chat, persistence, RAG, branching/parallelism, and small task‑oriented agents—so you can learn LangGraph by running real, minimal examples.

> **Why this repo?** To provide clear, reproducible, and copy‑pastable examples of LangGraph’s core ideas: **State**, **Nodes**, **Edges**, **Memory**, and **Control Flow**.

---

## ✨ Highlights

* Pure **notebook‑first** learning path: run, tweak, and observe.
* Covers **state persistence**, **looping**, **branching**, **parallelization**, and **RAG**.
* Lightweight, vendor‑agnostic: works with OpenAI, Groq, or any LangChain‑compatible LLM.
* Small utilities (BMI, Quadratic Equation) show how to turn classic problems into graphs.

---

## Prerequisites

* Python **3.10+**
* Jupyter Notebook or JupyterLab
* An LLM provider key (choose one):

  * `OPENAI_API_KEY` *(for `langchain-openai`)*, or
  * `GROQ_API_KEY` *(for `langchain-groq`)*

---

### Environment variables

Create a `.env` at repo root (or set in your shell):

```bash
OPENAI_API_KEY= # or GROQ_API_KEY=
LANGCHAIN_TRACING_V2=false
LANGCHAIN_PROJECT=langgraph-mini-projects
```

---

## Getting Started

1. **Clone** the repository

   ```bash
   git clone https://github.com/<your-username>/LangGraph_mini_projects.git
   cd LangGraph_mini_projects
   ```
2. **Set up** a virtual environment (recommended)

   ```bash
   python -m venv .venv && source .venv/bin/activate    # Windows: .venv\\Scripts\\activate
   ```
3. **Install** dependencies (see list above)
4. **Launch** Jupyter and open any notebook

   ```bash
   jupyter lab  # or: jupyter notebook
   ```

---

## Core Concepts Illustrated

* **State**: a typed dict/dataclass capturing inputs, intermediate fields, and outputs.
* **Nodes**: pure functions that read/write portions of state.
* **Edges**: control flow between nodes (`graph.add_edge`, conditional routing).
* **Memory**: chat history and domain memory (JSON/DB/Supabase/Vector DB).
* **Parallelism**: run independent nodes concurrently and merge results.
* **Loops/Iterations**: feedback‑driven refinement and stopping criteria.
* **RAG**: embed → store → retrieve → ground LLM answers with citations.

---

## Data & Persistence

* **Chatbot/** holds example conversations; some notebooks write JSON transcripts there.
* For RAG, vector stores are local by default (FAISS or Chroma). You can rewire to a managed DB if needed.
* When persisting, prefer a separate `data/` or `storage/` directory (git‑ignored) for large artifacts.

---

## Troubleshooting

* **Module not found**: ensure the virtual env is active and `pip show langgraph` works.
* **Rate limits / auth errors**: double‑check your API key and model name.
* **FAISS/Chroma not installed**: install the chosen vector store per the packages above.
* **Notebook out of order**: use *Kernel → Restart & Run All*.

---

## Contributing

Contributions are welcome—new notebooks, fixes, or improvements.

1. Fork → create a feature branch.
2. Add a new notebook following the naming convention.
3. Keep cells clean (minimal noise/output) and add a brief header cell with **Goal**, **Inputs**, **Outputs**.
4. Update the **Repository Structure** list above.
5. Open a PR with a short description and screenshots if useful.

---

## Acknowledgments

* Built with **LangGraph** + **LangChain**.
* Works with your choice of LLM provider (OpenAI, Groq, etc.).

> If this repo helps you, consider starring it and opening an issue with topics you’d like covered next (function calling, tools, graph persistence backends, multi‑agent orchestration, etc.).
