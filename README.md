# Awareness Short Generator

An AI agent that automates the full short-drama production pipeline — scriptwriting, scene breakdown, video generation, and editing — built for the Qwen Cloud AI Showrunner track.

## What it does
Given a topic and optional detailed scenes, the agent:
1. Generates a narrative script (Qwen text model)
2. Breaks it into structured scenes
3. Generates a video clip per scene (Wan video model, consistent style/seed)
4. Stitches all clips into one final video with smooth transitions

Includes a Streamlit web interface so non-technical users can generate videos by entering a topic.

## Demo
This project's demo output is a short film about a woman doctor's resilience after surviving an acid attack in Balochistan, Pakistan — made to raise awareness for acid attack survivors.

## Tech stack
- Python
- Qwen Cloud (qwen3.7-plus for script/scene generation)
- Wan2.7-t2v (video generation)
- MoviePy (video stitching)
- Streamlit (UI)

## How to run
1. `pip install openai dashscope moviepy streamlit requests`
2. Set your Qwen Cloud API key in `agent.py`
3. Run `streamlit run app.py`

## Files
- `agent.py` — core agent pipeline (script → scenes → video → stitch)
- `app.py` — Streamlit web interface
