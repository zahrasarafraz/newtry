# 🎤 PresentAI

PresentAI is a web app that helps you practise speeches. Upload a recording or record
with your microphone, and the app shows your **transcript**, your **speaking pace**
(words per minute) and your **filler words** (um, uh, like...).

It is a student project built with Python and Streamlit. The speech-to-text part runs
with [faster-whisper](https://github.com/SYSTRAN/faster-whisper), so no API key is needed.

## Features

- Upload an audio file (mp3, wav, m4a) or record with the microphone
- Transcript of the speech
- Speaking pace in WPM with simple feedback
- Filler word count and breakdown chart
- Project Information and About the Developer pages
- Your audio is not saved

## Project structure

```
presentai/
├── app.py                  # entry point: page setup and navigation
├── utils.py                # transcription, filler words, pace, audio checks
├── views/
│   ├── practice.py         # upload / record page
│   ├── project_info.py     # Project Information page
│   └── about_developer.py  # About the Developer page (fill in the placeholders)
├── .streamlit/config.toml  # colour theme and upload limit
├── requirements.txt        # Python packages
└── .gitignore
```

## Run it on your computer

You need Python 3.9 or newer. Use the same Python version that you will choose when you deploy.

**Mac**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

**Windows**
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The first analysis downloads the Whisper "base" model (about 150 MB), so it takes longer.

## Before you deploy: pin your versions

Deploy the versions you tested. In your activated environment run:

```
pip show streamlit faster-whisper pandas
```

Then change `requirements.txt` to exact versions, for example:

```
streamlit==X.Y.Z
faster-whisper==X.Y.Z
pandas==X.Y.Z
```

(Replace X.Y.Z with the numbers you see. Keep streamlit at 1.40 or newer.)

## Upload the project to GitHub

1. Create a new **public** repository on github.com (for example `presentai`).
2. In the project folder run:

```
git init
git add .
git commit -m "PresentAI first version"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/presentai.git
git push -u origin main
```

Check that no `.venv` folder, audio files or secrets were uploaded.

## Deploy on Streamlit Community Cloud

1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app** and choose your repository and the branch `main`.
3. Set the main file path to `app.py`.
4. Open **Advanced settings** and choose the same Python version you use on your computer.
5. Click **Deploy** and wait for the build to finish.
6. Test the live app: upload a file, record with the microphone, and try an empty recording.

Tips:
- Free apps go to sleep after a period without visitors. Open the app a few minutes
  before a demo so it can wake up and load the model.
- If the app shows "over its resource limits", open **Manage app → Logs**. A smaller
  model can help: in `utils.py` change `"base"` to `"tiny"` (less accurate, but lighter).
- Never put passwords or API keys in the repository.

## Limits of this version

- Whisper is not perfect, and filler word counts can vary slightly between attempts.
- Words like "so" and "like" are counted even when they are normal words.
- Recordings are limited to 5 minutes and files to 25 MB.
- Progress is not saved between visits.

## Possible future improvements

- AI coach feedback, volume and intonation analysis, saved progress, video analysis.
