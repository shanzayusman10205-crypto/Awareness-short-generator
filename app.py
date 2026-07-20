import streamlit as st
from agent import run_agent

st.set_page_config(page_title="Awareness Short Generator", page_icon="🎬")
st.title("🎬 Awareness Short Generator")

CHARACTER_ANCHOR = "A young Pakistani woman in her late 20s, warm brown eyes, black hair tied back or under a soft hijab, wearing a white doctor's coat over traditional shalwar kameez, gentle but determined expression."

LOCKED_STYLE = "2D hand-drawn animation style, clean bold outlines, flat cel-shading with soft warm lighting, muted color palette of terracotta, ochre, and sage green, painterly textured backgrounds, gentle cinematic framing, nostalgic storybook atmosphere"

topic = st.text_input("Topic", value="A woman doctor's journey and resilience after an acid attack in Balochistan, Pakistan")

use_manual = st.checkbox("Use my own detailed scenes", value=True)

manual_scenes = None
if use_manual:
    st.write("Enter each scene's visual description, one per line:")
    scene1 = st.text_area("Scene 1", "as a young girl age 10, hunched over worn textbooks by warm lamp light in a modest rural Balochistan home, dust motes floating in golden light, determined expression")
    scene2 = st.text_area("Scene 2", "quick match-cut montage growing older through medical school, studying, holding a stethoscope for the first time, tossing a graduation cap, warm nostalgic color grade")
    scene3 = st.text_area("Scene 3", "now working calmly in a small clinic in remote Balochistan, treating a patient, other women watching with quiet admiration, warm afternoon light through windows")
    scene4 = st.text_area("Scene 4", "sudden tonal shift to cold blue-grey lighting, an empty narrow street at dusk, a single overturned lamp flickering, a doctor's white coat dropped on the ground, wind moving fabric, silence")
    scene5 = st.text_area("Scene 5", "face now partially in soft shadow with a subtle scar near one eye, standing tall in her white coat again, back in her clinic, a patient reaching for her hand, warm light returning")

    manual_scenes = [
        {"narration": "", "visual_prompt": f"{CHARACTER_ANCHOR} {scene1}"},
        {"narration": "", "visual_prompt": f"{CHARACTER_ANCHOR} {scene2}"},
        {"narration": "", "visual_prompt": f"{CHARACTER_ANCHOR} {scene3}"},
        {"narration": "", "visual_prompt": scene4},
        {"narration": "", "visual_prompt": f"{CHARACTER_ANCHOR} {scene5}"},
    ]

if st.button("Generate Video", type="primary"):
    with st.spinner("Generating your short — this can take several minutes..."):
        try:
            final_video = run_agent(
                topic=topic,
                style=LOCKED_STYLE,
                manual_scenes=manual_scenes
            )
            st.success("Done!")
            st.video(final_video)
        except Exception as e:
            st.error(f"Something went wrong: {e}")