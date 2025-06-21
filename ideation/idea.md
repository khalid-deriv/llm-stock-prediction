Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea. Each question should build on my previous answers, and our end goal is to have a detailed specification I can hand off to an engineer. Let's do this iteratively and dig into every relevant detail. Remember, only one question at a time.
In addition, make sure you be concise with your questions and ask mainly necessary technical questions. The project must be a Minimum Lovable Product, with emphasis on minimalist build features and quick deployment. The focus is making ONE feature very simple and lovable and being minimalists with the rest of the product features.
Output would be: spec.md

Here's the idea: An LLM AI that predicts stock prices
The AI has a personality as a super accurate stock data analyst. Its level of expertise is vast and broad, yet deep. It takes in the following inputs:

**Input**:
1. Stock data for the last 3 years (data.json/data.csv)
2. Instructions file as LLM context (instructions.md)

**Output**:
1. 1 year stock data prediction
2. Top 10 profitable price movements prediction
3. Explanation for the top 10 predictions and the resoning behind it
