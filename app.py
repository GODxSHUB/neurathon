
import streamlit as st
import json
import pyaudio
from datetime import datetime
from vosk import Model, KaldiRecognizer
from styles import apply_custom_css
from llm_helper import get_ai_steps

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Companion",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply CSS
apply_custom_css()

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "mood_selection"
if "points" not in st.session_state:
    st.session_state.points = 47
if "steps" not in st.session_state:
    st.session_state.steps = []
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = 3
if "streak_days" not in st.session_state:
    st.session_state.streak_days = 5
if "mood" not in st.session_state:
    st.session_state.mood = None
if "task_started" not in st.session_state:
    st.session_state.task_started = False
if "task_input_val" not in st.session_state:
    st.session_state.task_input_val = ""
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

# ---------------- VOSK VOICE FUNCTION ----------------
def record_voice():
    model_path = "model"
    if not st.session_state.is_recording:
        return None

    try:
        model = Model(model_path)
        rec = KaldiRecognizer(model, 16000)
        
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()
        
        placeholder = st.empty()
        placeholder.info("🎤 Listening... Speak now!")
        
        import time
        start_time = time.time()
        final_text = ""
        
        while time.time() - start_time < 5: 
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                final_text += res.get('text', '') + " "
        
        res = json.loads(rec.FinalResult())
        final_text += res.get('text', '')
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        placeholder.empty()
        
        return final_text.strip()

    except Exception as e:
        st.error(f"Error: {e}. Check if 'model' folder exists.")
        return None

# ==================== PAGE 1: MOOD SELECTION ====================
if st.session_state.page == "mood_selection":
    
    st.markdown("<h1 style='text-align: center;'>Smart Companion</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #4B5563; margin-bottom: 40px;'>AI-Powered Task Management for Neurodivergent Minds</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c2:
        st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>How are you feeling today?</h3>", unsafe_allow_html=True)
        
        row1_1, row1_2 = st.columns(2)
        row2_1, row2_2 = st.columns(2)
        
        def mood_btn(col, text):
            with col:
                if st.button(text, use_container_width=True):
                    st.session_state.mood = text.split(" ")[1] 
                    
        mood_btn(row1_1, "🙂 Calm")
        mood_btn(row1_2, "😴 Low Energy")
        mood_btn(row2_1, "😣 Overwhelmed")
        mood_btn(row2_2, "🔥 Motivated")
        
        if st.session_state.mood:
            st.markdown(f"<p style='text-align:center; margin-top:20px; font-weight:bold; color:#7C3AED;'>Selected: {st.session_state.mood}</p>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            
            if st.button("Proceed ➔", key="proceed_btn", type="primary", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()

# ==================== PAGE 2: DASHBOARD ====================
elif st.session_state.page == "dashboard":
    
    st.markdown("<h1 style='margin-bottom: 10px;'>Smart Companion</h1>", unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 1.8, 1])
    
    # --- LEFT: INPUT ---
    with col_left:
        st.markdown("<h3>What needs to be done?</h3>", unsafe_allow_html=True)
        
        if st.button("🎤 Record Voice (5s)", use_container_width=True):
            st.session_state.is_recording = True
            text_out = record_voice()
            if text_out:
                st.session_state.task_input_val = text_out
            st.session_state.is_recording = False
            st.rerun()

        task_input = st.text_area(
            "task", 
            value=st.session_state.task_input_val, 
            placeholder="Type here or use voice...", 
            height=150, 
            label_visibility="collapsed"
        )
        
        if task_input != st.session_state.task_input_val:
            st.session_state.task_input_val = task_input

        if st.button("✨ Generate Action Plan", use_container_width=True, type="primary"):
            if st.session_state.task_input_val:
                with st.spinner("Breaking it down..."):
                    st.session_state.steps = get_ai_steps(st.session_state.task_input_val, st.session_state.mood)
                    st.session_state.task_started = True
                    st.session_state.current_step = 0
                st.rerun()
            
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "mood_selection"
            st.rerun()

    # --- CENTER: ACTIVE TASK ---
    with col_center:
        if st.session_state.task_started and st.session_state.steps:
            total = len(st.session_state.steps)
            curr = st.session_state.current_step
            
            s1, s2, s3 = st.columns(3)
            with s1: st.markdown(f"**Step {curr+1}/{total}**")
            with s2: st.markdown(f"**{int(curr/total*100)}% Done**")
            with s3: st.markdown(f"**~{(total-curr)*2} min**")
            
            st.progress(curr/total if total > 0 else 0)
            
            if curr < total:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.6); padding: 30px; border-radius: 20px; 
                            border-left: 6px solid #8B5CF6; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <div style='background:#EDE9FE; color:#8B5CF6; padding:5px 12px; border-radius:6px; display:inline-block; font-weight:bold; font-size:0.8rem;'>NEXT ACTION</div>
                    <div style='float:right; font-size:1.8rem; font-weight:800; color:#E5E7EB;'>#{curr+1}</div>
                    <p style='font-size: 1.6rem; font-weight: 600; margin-top: 20px; line-height: 1.3; color: #1F2937;'>
                        {st.session_state.steps[curr]}
                    </p>
                    <p style='color: #6B7280; font-size: 0.9rem; margin-top: 15px;'>⏱ ~2 minutes</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<div style='height: 15px'></div>", unsafe_allow_html=True)
                
                if st.button("✓ Mark as Complete", use_container_width=True, type="primary"):
                    st.session_state.current_step += 1
                    st.session_state.points += 5
                    if st.session_state.current_step >= total:
                        st.session_state.completed_tasks += 1
                        st.balloons()
                    st.rerun()
                
                if curr + 1 < total:
                    st.markdown("<div style='margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.3); border-radius: 12px;'>", unsafe_allow_html=True)
                    st.markdown("**Coming Up:**")
                    for i in range(curr+1, min(curr+3, total)):
                        st.markdown(f"<span style='color:#4B5563; display:block; margin-top:5px;'>• {st.session_state.steps[i]}</span>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='text-align:center; margin-top:50px;'><h2>🎉 All Done!</h2><p>Take a break.</p></div>", unsafe_allow_html=True)
        else:
             st.markdown("<div style='text-align:center; padding:50px; opacity:0.6;'><h3>Ready to Focus?</h3><p>Enter a task on the left.</p></div>", unsafe_allow_html=True)

    # --- RIGHT: STATS ---
    with col_right:
        st.markdown("<h3>Today's Progress</h3>", unsafe_allow_html=True)
        
        st.markdown("<div style='margin-bottom: 15px;'>", unsafe_allow_html=True)
        st.markdown("<p class='label-stat'>POINTS EARNED</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='big-stat' style='color:#F59E0B;'>{st.session_state.points}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border: 0; border-top: 1px solid rgba(0,0,0,0.1); margin: 10px 0;'>", unsafe_allow_html=True)
        
        st.markdown("<div style='margin-bottom: 15px;'>", unsafe_allow_html=True)
        st.markdown("<p class='label-stat'>TASKS COMPLETED</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='big-stat' style='color:#10B981;'>{st.session_state.completed_tasks}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border: 0; border-top: 1px solid rgba(0,0,0,0.1); margin: 10px 0;'>", unsafe_allow_html=True)
        
        st.markdown("<p class='label-stat'>CURRENT STREAK</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 1.5rem; font-weight:700; color:#F97316;'>🔥 {st.session_state.streak_days} Days</p>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background:rgba(139, 92, 246, 0.1); padding:15px; border-radius:12px; margin-top:20px;'>
            <p style='color:#7C3AED; font-weight:bold; margin:0; font-size:0.9rem;'>LEVEL: Task Starter</p>
            <p style='font-size:0.8rem; margin:5px 0 0 0;'>47/100 XP to next level</p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- JSON SECTION ---
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        
        # 1. Prepare Data
        export_data = {
            "timestamp": str(datetime.now()),
            "user_stats": {
                "points": st.session_state.points,
                "completed_tasks": st.session_state.completed_tasks,
                "streak_days": st.session_state.streak_days
            },
            "current_session": {
                "mood": st.session_state.mood,
                "task": st.session_state.task_input_val,
                "progress": f"{st.session_state.current_step}/{len(st.session_state.steps)}",
                "steps": st.session_state.steps
            }
        }
        json_str = json.dumps(export_data, indent=4)
        
        # 2. Show Data Option (NEW)
        with st.expander("👁️ Show Raw Data"):
            st.json(export_data)

        # 3. Download Button
        st.download_button(
            label="💾 Download Progress (JSON)",
            data=json_str,
            file_name="smart_companion_data.json",
            mime="application/json",
            use_container_width=True
        )

# Footer
st.markdown("""
    <div style='position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; padding: 15px; background: rgba(255,255,255,0.5); backdrop-filter: blur(5px); font-size: 0.9rem; font-weight: 600; color: #000000;'>
        Made with 💗 team NeuralNodes
    </div>
""", unsafe_allow_html=True)




















# import streamlit as st
# import json
# import pyaudio
# from vosk import Model, KaldiRecognizer
# from styles import apply_custom_css
# from llm_helper import get_ai_steps

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="Smart Companion",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Apply CSS
# apply_custom_css()

# # ---------------- SESSION STATE ----------------
# if "page" not in st.session_state:
#     st.session_state.page = "mood_selection"
# if "points" not in st.session_state:
#     st.session_state.points = 47
# if "steps" not in st.session_state:
#     st.session_state.steps = []
# if "current_step" not in st.session_state:
#     st.session_state.current_step = 0
# if "completed_tasks" not in st.session_state:
#     st.session_state.completed_tasks = 3
# if "streak_days" not in st.session_state:
#     st.session_state.streak_days = 5
# if "mood" not in st.session_state:
#     st.session_state.mood = None
# if "task_started" not in st.session_state:
#     st.session_state.task_started = False
# if "task_input_val" not in st.session_state:
#     st.session_state.task_input_val = ""
# if "is_recording" not in st.session_state:
#     st.session_state.is_recording = False

# # ---------------- VOSK VOICE FUNCTION ----------------
# def record_voice():
#     model_path = "model"  # Ensure folder is named 'model'
    
#     if not st.session_state.is_recording:
#         return None

#     try:
#         model = Model(model_path)
#         rec = KaldiRecognizer(model, 16000)
        
#         p = pyaudio.PyAudio()
#         stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
#         stream.start_stream()
        
#         placeholder = st.empty()
#         placeholder.info("🎤 Listening... Speak now!")
        
#         # Record for fixed duration (e.g. 5 seconds) or untill silence (simplified here for 4s)
#         # For a production app, you'd want a "Stop" button logic, but that requires async in Streamlit
#         # Here we record for ~5 seconds for simplicity in this demo.
#         import time
#         start_time = time.time()
#         final_text = ""
        
#         while time.time() - start_time < 5: 
#             data = stream.read(4000, exception_on_overflow=False)
#             if rec.AcceptWaveform(data):
#                 res = json.loads(rec.Result())
#                 final_text += res.get('text', '') + " "
        
#         # Get final bit
#         res = json.loads(rec.FinalResult())
#         final_text += res.get('text', '')
        
#         stream.stop_stream()
#         stream.close()
#         p.terminate()
#         placeholder.empty()
        
#         return final_text.strip()

#     except Exception as e:
#         st.error(f"Error: {e}. Check if 'model' folder exists.")
#         return None

# # ==================== PAGE 1: MOOD SELECTION ====================
# if st.session_state.page == "mood_selection":
    
#     st.markdown("<h1 style='text-align: center;'>Smart Companion</h1>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center; color: #4B5563; margin-bottom: 40px;'>AI-Powered Task Management for Neurodivergent Minds</p>", unsafe_allow_html=True)
    
#     c1, c2, c3 = st.columns([1, 2, 1])
    
#     with c2:
#         st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>How are you feeling today?</h3>", unsafe_allow_html=True)
        
#         row1_1, row1_2 = st.columns(2)
#         row2_1, row2_2 = st.columns(2)
        
#         def mood_btn(col, text):
#             with col:
#                 if st.button(text, use_container_width=True):
#                     st.session_state.mood = text.split(" ")[1] 
                    
#         mood_btn(row1_1, "🙂 Calm")
#         mood_btn(row1_2, "😴 Low Energy")
#         mood_btn(row2_1, "😣 Overwhelmed")
#         mood_btn(row2_2, "🔥 Motivated")
        
#         if st.session_state.mood:
#             st.markdown(f"<p style='text-align:center; margin-top:20px; font-weight:bold; color:#7C3AED;'>Selected: {st.session_state.mood}</p>", unsafe_allow_html=True)
#             st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            
#             if st.button("Proceed ➔", key="proceed_btn", type="primary", use_container_width=True):
#                 st.session_state.page = "dashboard"
#                 st.rerun()

# # ==================== PAGE 2: DASHBOARD ====================
# elif st.session_state.page == "dashboard":
    
#     st.markdown("<h1 style='margin-bottom: 10px;'>Smart Companion</h1>", unsafe_allow_html=True)
    
#     col_left, col_center, col_right = st.columns([1, 1.8, 1])
    
#     # --- LEFT: INPUT ---
#     with col_left:
#         st.markdown("<h3>What needs to be done?</h3>", unsafe_allow_html=True)
        
#         # --- VOSK RECORD BUTTON ---
#         # When clicked, we trigger recording
#         if st.button("🎤 Record Voice (5s)", use_container_width=True):
#             st.session_state.is_recording = True
#             text_out = record_voice()
#             if text_out:
#                 st.session_state.task_input_val = text_out
#             st.session_state.is_recording = False
#             st.rerun()

#         # --- TEXT AREA ---
#         # Bind value to session state
#         task_input = st.text_area(
#             "task", 
#             value=st.session_state.task_input_val, 
#             placeholder="Type here or use voice...", 
#             height=150, 
#             label_visibility="collapsed"
#         )
        
#         # Keep state in sync if user types manually
#         if task_input != st.session_state.task_input_val:
#             st.session_state.task_input_val = task_input

#         # Generate Button
#         if st.button("✨ Generate Action Plan", use_container_width=True, type="primary"):
#             if st.session_state.task_input_val:
#                 with st.spinner("Breaking it down..."):
#                     st.session_state.steps = get_ai_steps(st.session_state.task_input_val, st.session_state.mood)
#                     st.session_state.task_started = True
#                     st.session_state.current_step = 0
#                 st.rerun()
            
#         if st.button("← Back", use_container_width=True):
#             st.session_state.page = "mood_selection"
#             st.rerun()

#     # --- CENTER: ACTIVE TASK ---
#     with col_center:
#         if st.session_state.task_started and st.session_state.steps:
#             total = len(st.session_state.steps)
#             curr = st.session_state.current_step
            
#             s1, s2, s3 = st.columns(3)
#             with s1: st.markdown(f"**Step {curr+1}/{total}**")
#             with s2: st.markdown(f"**{int(curr/total*100)}% Done**")
#             with s3: st.markdown(f"**~{(total-curr)*2} min**")
            
#             st.progress(curr/total if total > 0 else 0)
            
#             if curr < total:
#                 st.markdown(f"""
#                 <div style="background: rgba(255,255,255,0.6); padding: 30px; border-radius: 20px; 
#                             border-left: 6px solid #8B5CF6; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
#                     <div style='background:#EDE9FE; color:#8B5CF6; padding:5px 12px; border-radius:6px; display:inline-block; font-weight:bold; font-size:0.8rem;'>NEXT ACTION</div>
#                     <div style='float:right; font-size:1.8rem; font-weight:800; color:#E5E7EB;'>#{curr+1}</div>
#                     <p style='font-size: 1.6rem; font-weight: 600; margin-top: 20px; line-height: 1.3; color: #1F2937;'>
#                         {st.session_state.steps[curr]}
#                     </p>
#                     <p style='color: #6B7280; font-size: 0.9rem; margin-top: 15px;'>⏱ ~2 minutes</p>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#                 st.markdown("<div style='height: 15px'></div>", unsafe_allow_html=True)
                
#                 if st.button("✓ Mark as Complete", use_container_width=True, type="primary"):
#                     st.session_state.current_step += 1
#                     st.session_state.points += 5
#                     if st.session_state.current_step >= total:
#                         st.session_state.completed_tasks += 1
#                         st.balloons()
#                     st.rerun()
                
#                 if curr + 1 < total:
#                     st.markdown("<div style='margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.3); border-radius: 12px;'>", unsafe_allow_html=True)
#                     st.markdown("**Coming Up:**")
#                     for i in range(curr+1, min(curr+3, total)):
#                         st.markdown(f"<span style='color:#4B5563; display:block; margin-top:5px;'>• {st.session_state.steps[i]}</span>", unsafe_allow_html=True)
#                     st.markdown("</div>", unsafe_allow_html=True)
#             else:
#                 st.markdown("<div style='text-align:center; margin-top:50px;'><h2>🎉 All Done!</h2><p>Take a break.</p></div>", unsafe_allow_html=True)
#         else:
#              st.markdown("<div style='text-align:center; padding:50px; opacity:0.6;'><h3>Ready to Focus?</h3><p>Enter a task on the left.</p></div>", unsafe_allow_html=True)

#     # --- RIGHT: STATS ---
#     with col_right:
#         st.markdown("<h3>Today's Progress</h3>", unsafe_allow_html=True)
        
#         st.markdown("<div style='margin-bottom: 15px;'>", unsafe_allow_html=True)
#         st.markdown("<p class='label-stat'>POINTS EARNED</p>", unsafe_allow_html=True)
#         st.markdown(f"<p class='big-stat' style='color:#F59E0B;'>{st.session_state.points}</p>", unsafe_allow_html=True)
#         st.markdown("</div>", unsafe_allow_html=True)
        
#         st.markdown("<hr style='border: 0; border-top: 1px solid rgba(0,0,0,0.1); margin: 10px 0;'>", unsafe_allow_html=True)
        
#         st.markdown("<div style='margin-bottom: 15px;'>", unsafe_allow_html=True)
#         st.markdown("<p class='label-stat'>TASKS COMPLETED</p>", unsafe_allow_html=True)
#         st.markdown(f"<p class='big-stat' style='color:#10B981;'>{st.session_state.completed_tasks}</p>", unsafe_allow_html=True)
#         st.markdown("</div>", unsafe_allow_html=True)
        
#         st.markdown("<hr style='border: 0; border-top: 1px solid rgba(0,0,0,0.1); margin: 10px 0;'>", unsafe_allow_html=True)
        
#         st.markdown("<p class='label-stat'>CURRENT STREAK</p>", unsafe_allow_html=True)
#         st.markdown(f"<p style='font-size: 1.5rem; font-weight:700; color:#F97316;'>🔥 {st.session_state.streak_days} Days</p>", unsafe_allow_html=True)
        
#         st.markdown(f"""
#         <div style='background:rgba(139, 92, 246, 0.1); padding:15px; border-radius:12px; margin-top:20px;'>
#             <p style='color:#7C3AED; font-weight:bold; margin:0; font-size:0.9rem;'>LEVEL: Task Starter</p>
#             <p style='font-size:0.8rem; margin:5px 0 0 0;'>47/100 XP to next level</p>
#         </div>
#         """, unsafe_allow_html=True)

# # Footer
# st.markdown("<div style='position:fixed; bottom:10px; right:10px; font-size:0.8rem; color:#6B7280;'>Made with 💗</div>", unsafe_allow_html=True)