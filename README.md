# AMSL Agentic AI Study Portal

Korean student-facing study portal for the AMSL internship Agentic AI module.

The public page is the textbook. The downloadable ZIP is the runnable practice
package with `START_HERE.md`, `requirements.txt`, and Section 0-5 Jupyter
notebooks.

## Audience

- AMSL interns using Windows and PowerShell.
- Students who know basic Python but are new to LLM API development.
- Learners preparing for structured output, Pydantic validation, RAG, and
  workflow-style agent building.

## Public URL

```text
https://intern-study.donghyunlee.me
```

Before sharing, confirm the custom-domain HTTPS certificate is valid for this
hostname.

## Local Preview

```bash
cd /data/openclaw/workspace/amsl-internship-study
PYTHONDONTWRITEBYTECODE=1 python3 serve.py
```

Open:

```text
http://127.0.0.1:8767
```

## Contents

- `index.html`: public study page.
- `START_HERE.md`: quickstart included in the ZIP.
- `requirements.txt`: notebook dependencies.
- `notebooks/`: runnable Section notebooks.
- `downloads/amsl-internship-practice-files.zip`: student download package.
- `serve.py`: local UTF-8 static server.

## Update Checklist

1. Edit `index.html`, `START_HERE.md`, `requirements.txt`, or notebooks.
2. Make sure notebook examples match the page claims.
3. Clear notebook outputs and execution counts before packaging.
4. Confirm there are no real API keys or private values in notebooks.
5. Rebuild `downloads/amsl-internship-practice-files.zip`.
6. Check the page, ZIP, anchors, and notebook JSON locally.

## Secret Safety

Students paste the class API key directly into notebook cells to reduce setup
friction. A saved notebook can keep that key in the file. Before sharing,
submitting, committing, or screen sharing, clear the API key cell and notebook
outputs.
