from openai import OpenAI
import os
import dashscope
from dashscope import VideoSynthesis
from moviepy import VideoFileClip, concatenate_videoclips, vfx
import requests

# --- Setup ---
API_KEY = "YOUR_API_KEY_HERE"
dashscope.api_key = API_KEY
dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

# --- Step 1: Script generation ---
def generate_script(topic, key_message="", tone="hopeful and respectful", length="60-90 seconds"):
    prompt = f"""
    Write a short animated awareness video script about: {topic}
    Key message to include: {key_message if key_message else "use your judgment on the most important message"}
    Tone: {tone}
    Target length: {length}
    Break it into scenes. For each scene provide:
    - Narration line
    - Visual description (symbolic/artistic, non-graphic, suitable for AI video generation)
    Format as a numbered list of scenes.
    """
    response = client.chat.completions.create(
        model="qwen3.7-plus",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# --- Step 2: Parse into structured scenes ---
def generate_scenes(script_text, manual_scenes=None):
    if manual_scenes:
        return manual_scenes

    prompt = f"""
    Convert this script into a JSON list of scenes. Each item should have:
    "narration" and "visual_prompt" fields only.

    IMPORTANT: In each scene's "visual_prompt" (except the first), explicitly describe
    how the visual continues or connects from the previous scene's ending (e.g. same
    character position, same location transitioning, same lighting mood carrying over),
    so the scenes feel like one continuous sequence rather than disconnected shots.

    Script:
    {script_text}
    Respond ONLY with valid JSON, no other text.
    """
    response = client.chat.completions.create(
        model="qwen3.7-plus",
        messages=[{"role": "user", "content": prompt}]
    )
    import json
    clean = response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


# --- Step 3: Video generation per scene ---
def generate_video_clip(visual_prompt, style, index=0, seed=42):
    full_prompt = f"{visual_prompt}, {style}"
    response = VideoSynthesis.async_call(
        model="wan2.7-t2v",
        prompt=full_prompt,
        seed=seed,
        audio=False
    )
    result = VideoSynthesis.wait(response)
    video_url = result.output.video_url
    file_path = f"scene_{index}.mp4"

    for attempt in range(3):
        try:
            video_data = requests.get(video_url, timeout=60).content
            with open(file_path, "wb") as f:
                f.write(video_data)
            return file_path
        except requests.exceptions.ConnectionError:
            print(f"Download attempt {attempt+1} failed, retrying...")
            import time
            time.sleep(5)

    raise Exception(f"Failed to download video after 3 attempts: {video_url}")



# --- Step 4: Stitch everything together ---
def stitch_clips(clip_paths, output_path="final_output.mp4", fade_duration=0.5):
    clips = [VideoFileClip(p).without_audio() for p in clip_paths]
    clips_faded = [clips[0]] + [c.with_effects([vfx.CrossFadeIn(fade_duration)]) for c in clips[1:]]
    final = concatenate_videoclips(clips_faded, method="compose", padding=-fade_duration)
    final.write_videofile(output_path)
    return output_path


# --- Main orchestrator ---
def run_agent(topic, key_message="", tone="hopeful and respectful", length="60-90 seconds",
              style="2D hand-drawn animation style, clean bold outlines, flat cel-shading with soft warm lighting, muted color palette of terracotta, ochre, and sage green, painterly textured backgrounds, gentle cinematic framing, nostalgic storybook atmosphere", manual_scenes=None):

    print("Generating script...")
    script = generate_script(topic, key_message, tone, length)

    print("Breaking into scenes...")
    scenes = generate_scenes(script, manual_scenes)
    scenes = scenes[:3]  # TEMP: limit to 3 scenes for testing

    print(f"Generating {len(scenes)} video clips...")
    clip_paths = []
    for i, scene in enumerate(scenes):
        path = generate_video_clip(scene["visual_prompt"], style, i)
        clip_paths.append(path)

    print("Stitching final video...")
    final = stitch_clips(clip_paths)

    print(f"Done! Final video: {final}")
    return final

def extract_last_frame(video_path, output_image="last_frame.png"):
    clip = VideoFileClip(video_path)
    clip.save_frame(output_image, t=clip.duration - 0.1)
    return output_image


if __name__ == "__main__":
    run_agent(
        topic="a lighthouse keeper waiting for a ship that never comes",
        key_message="hope persists even in solitude",
        tone="calm, poetic",
        style="2D hand-drawn animation style, clean bold outlines, flat cel-shading with soft warm lighting, muted color palette of terracotta, ochre, and sage green, painterly textured backgrounds, gentle cinematic framing, nostalgic storybook atmosphere"
    )
