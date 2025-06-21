GitHub Copilot: ```markdown
# LLM Stock Prediction MVP — Step-by-Step Blueprint & Prompts

This document provides a detailed, incremental blueprint for building the LLM Stock Prediction MVP as described in `spec.md`. Each section breaks the project into small, testable, and iterative steps, with prompts for a code-generation LLM to implement each part using best practices and early testing.

---

## 1. High-Level Blueprint

### 1.1. Project Initialization
- Set up a new Django project and app with minimal configuration.
- Configure Postgres for authentication only.
- Set up static and media file handling for temporary file storage.
- Add HTMX and minimal frontend dependencies.

### 1.2. Authentication
- Implement minimalist Django authentication (login/signup/logout).
- Use HTMX for seamless UI updates.

### 1.3. File Upload & Management
- Implement upload forms for CSV stock data and instructions.md.
- Provide default sample files.
- Store uploads in temporary storage (not DB).

### 1.4. Instructions Management
- Display default instructions.
- Allow user to upload and view their own instructions.md.

### 1.5. LLM Integration
- Integrate Langchain for LLM API interaction.
- Support pluggable API key and web-enabled LLMs.
- Implement persona prompt logic.

### 1.6. Prediction Workflow
- On submission, send stock data and instructions to LLM.
- Receive and parse LLM output (prediction.csv, top 10 table, explanations).

### 1.7. Output Display
- Display top 10 predictions and explanations in a table.
- Render combined line chart for top 10 stocks (12 months).
- Provide download link for prediction.csv.

### 1.8. Testing & Deployment
- Add unit and integration tests for each component.
- Prepare for quick deployment (minimal dependencies).

---

## 2. Iterative Chunks

### Chunk 1: Project Setup
- Initialize Django project and app.
- Configure Postgres for auth.
- Set up static/media files and HTMX.

### Chunk 2: Authentication
- Implement login/signup/logout views and templates.
- Test authentication flow.

### Chunk 3: File Uploads
- Create upload forms for CSV and instructions.md.
- Store files temporarily.
- Provide sample files.

### Chunk 4: Instructions Management
- Display default instructions.
- Allow upload/view of custom instructions.md.

### Chunk 5: LLM Integration
- Integrate Langchain.
- Set up API key config.
- Implement persona prompt logic.

### Chunk 6: Prediction Workflow
- Send data/instructions to LLM.
- Parse and validate LLM output.

### Chunk 7: Output Display
- Show top 10 predictions/explanations in table.
- Render combined line chart.
- Provide download for prediction.csv.

### Chunk 8: Testing & Deployment
- Add tests for each feature.
- Prepare deployment scripts.

---

## 3. Further Breakdown (Small Steps)

### Chunk 1: Project Setup
1. Initialize Django project.
2. Create Django app (e.g., `predictor`).
3. Configure Postgres in `settings.py`.
4. Set up static and media file handling.
5. Add HTMX to base template.

### Chunk 2: Authentication
1. Scaffold User model (use Django default).
2. Create signup view/template.
3. Create login view/template.
4. Create logout view.
5. Add tests for auth flow.

### Chunk 3: File Uploads
1. Create upload form for CSV.
2. Create upload form for instructions.md.
3. Store files in `/tmp` or similar.
4. Provide sample files for download.
5. Add tests for upload logic.

### Chunk 4: Instructions Management
1. Display default instructions.md.
2. Allow user to view uploaded instructions.
3. Add tests for instructions logic.

### Chunk 5: LLM Integration
1. Install and configure Langchain.
2. Add API key config (env var).
3. Implement persona prompt builder.
4. Add tests for prompt logic.

### Chunk 6: Prediction Workflow
1. On form submit, send files and prompt to LLM.
2. Receive and parse LLM output (CSV, table, explanations).
3. Validate output format.
4. Add tests for workflow.

### Chunk 7: Output Display
1. Display top 10 predictions in table.
2. Show explanations.
3. Render combined line chart (e.g., Chart.js).
4. Provide download link for prediction.csv.
5. Add tests for output rendering.

### Chunk 8: Testing & Deployment
1. Add unit/integration tests for all features.
2. Write deployment instructions/scripts.
3. Test end-to-end flow.

---

## 4. Prompts for Code-Generation LLM

### Prompt 1: Project Setup
```text
Create a new Django project and app named `predictor`. Configure Postgres as the database for authentication only. Set up static and media file handling for temporary file storage. Add HTMX to the base template for frontend interactivity. Ensure the project runs locally with minimal dependencies.
```

### Prompt 2: Authentication
```text
Implement minimalist authentication using Django’s built-in User model. Create signup, login, and logout views and templates using HTMX for seamless UI updates. Add tests to verify the authentication flow.
```

### Prompt 3: File Uploads
```text
Create forms and views to upload a CSV file (stock data) and an instructions.md file. Store uploaded files in a temporary directory (not in the database). Provide sample files for download. Add tests to ensure file uploads and downloads work correctly.
```

### Prompt 4: Instructions Management
```text
Display the default instructions.md file in the UI. Allow users to view their uploaded instructions.md file if present. Add tests to verify instructions display and upload logic.
```

### Prompt 5: LLM Integration
```text
Integrate Langchain for LLM API interaction. Allow configuration of the API key via environment variable. Implement logic to build the persona prompt as specified in the spec. Add tests to verify prompt construction and API key configuration.
```

### Prompt 6: Prediction Workflow
```text
On form submission, send the uploaded CSV and instructions.md (or default) to the LLM using Langchain. Receive the LLM’s output: a prediction.csv file (top 10 stocks, 12 months each), a table of top 10 predictions, and explanations. Parse and validate the output. Add tests for the workflow and output validation.
```

### Prompt 7: Output Display
```text
Display the top 10 predictions and their explanations in a table in the UI. Render a combined line chart (e.g., using Chart.js) showing predicted prices for all 10 stocks over 12 months. Provide a download link for the prediction.csv file. Add tests for output rendering and download functionality.
```

### Prompt 8: Testing & Deployment
```text
Add comprehensive unit and integration tests for all features. Write deployment instructions and scripts for quick setup. Test the end-to-end flow to ensure all components work together as specified.
```

---

## 5. Review & Right-Sizing

- Each chunk is broken into atomic, testable steps.
- Prompts are sequential and build on previous work.
- No orphaned or unintegrated code at any stage.
- Early testing is prioritized for each feature.
- Final prompt wires all components together for a working MVP.

---

**This blueprint and prompt set can be handed off to a code-generation LLM or engineering team for safe, incremental, and test-driven implementation.**
```
