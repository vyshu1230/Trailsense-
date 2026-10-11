# TrailSense: From Screen to Soil

A beginner garden helper that gets people off the screen and into the garden. It runs fully on a laptop with open-weight AI, with no internet and no account needed.

Built for the DEV **Touch Grass** challenge.

## What it does

- **Find Plants:** suggests beginner plants that fit your space, sunlight, budget and daily care time, each with a match score and reasons.
- **My Garden:** save plants, get a small daily task for each one, mark tasks complete, and remove plants. Your garden is saved in a local file.
- **AI Assistant:** ask a gardening question and get a short answer in simple words, ending with one 5-minute outdoor task. The answer uses your sidebar setup and the plants you have saved.

## Open-source AI

- **Model:** `llama3.2`, an open-weight model, run locally with [Ollama](https://ollama.com).
- **Interface:** [Streamlit](https://streamlit.io).
- **Privacy and cost:** nothing is sent to a server. Your garden data stays in `garden_progress.json` on your own machine, and it costs nothing to run.
- **Swap models:** change the `AI_MODEL` line near the top of `web_app.py` to any model shown by `ollama list`.

## How to run

1. Install [Ollama](https://ollama.com) and download the model:
   ```
   ollama pull llama3.2
   ```
2. Install Python, then install the libraries:
   ```
   pip install -r requirements.txt
   ```
3. Start the app:
   ```
   python -m streamlit run web_app.py
   ```
4. Open `http://localhost:8501` in your browser.

## Files

- `web_app.py`: the whole app
- `plants.json`: the plant data
- `garden_progress.json`: your saved garden (starts empty)
- `requirements.txt`: Python libraries

## Known limits

- A small local model can make mistakes, so treat plant advice as a starting point, not expert advice.
-  A vague answer or a wrong detail.
- We have not yet tested it outdoors in a real garden. That is our next step.

## Team

- @vyshu1230:  designed and built the app
- @Himacharan69: found and fixed the missing AI Assistant page, tested the app.
- @pashya_rishitha_0610:helped in designing the app.
