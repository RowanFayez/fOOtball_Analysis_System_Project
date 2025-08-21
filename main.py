import streamlit as st
import cv2
import numpy as np
from utils import frames_to_video_bytes, process_video
from trackers import Tracker
from TeamAssigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner

@st.cache_resource
def load_tracker(model_path):
    """Cache the YOLO model to avoid reloading on every run"""
    try:
        tracker = Tracker(model_path)
        return tracker
    except Exception as e:
        st.error(f"Error loading model from {model_path}: {str(e)}")
        return None


@st.cache_resource
def load_team_assigner():
    """Cache the team assigner to avoid recreation"""
    try:
        return TeamAssigner()
    except Exception as e:
        st.error(f"Error initializing TeamAssigner: {str(e)}")
        return None


@st.cache_resource
def load_player_ball_assigner():
    try:
        return PlayerBallAssigner()
    except Exception as e:
        st.error(f"Error initializing PlayerBallAssigner: {str(e)}")
        return None



def add_theme():
    """Inject sporty stadium night CSS styling"""
    st.markdown("""
        <style>
        /* Main app background: darker night stadium */
        .stApp {
            background: linear-gradient(rgba(0, 0, 30, 0.85), rgba(0, 0, 20, 0.95)),
                        url('https://images.stockcake.com/public/9/e/e/9eebde67-5b64-42cf-9cb5-41c3bbd821de_large/stadium-lights-glow-stockcake.jpg');
            background-size: cover;
            background-attachment: fixed;
            color: #e0e0e0 !important;
        }

        /* Headings with LED scoreboard glow */
        h1, h2, h3, h4 {
            font-family: "Trebuchet MS", sans-serif;
            font-weight: bold;
            color: #00c8ff !important; /* Cyan LED */
            text-shadow: 2px 2px 12px #001f3f;
            letter-spacing: 1px;
        }

        /* Sidebar: metallic tunnel look */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #111, #222);
            border-right: 3px solid #00c8ff;
            color: #f0f0f0;
        }
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
            color: #00c8ff !important;
        }

        /* Buttons: glowing neon panels */
        .stButton>button {
            background: linear-gradient(145deg, #003366, #005599);
            color: white;
            border-radius: 20px;
            border: 2px solid #00c8ff;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 0.5em 1em;
            box-shadow: 0 0 8px #00c8ff;
            transition: 0.2s ease-in-out;
        }
        .stButton>button:hover {
            background: linear-gradient(145deg, #00c8ff, #003366);
            color: black;
            border-color: white;
            box-shadow: 0 0 12px #00c8ff;
        }

        /* Radio buttons (Fast / Balanced / Slow) */
        div[role="radiogroup"] label {
            background: #002244;
            border: 2px solid #00c8ff;
            border-radius: 15px;
            padding: 8px 15px;
            margin: 4px;
            font-weight: bold;
            color: white !important;
            box-shadow: 0 0 6px #00c8ff;
        }
        div[role="radiogroup"] label:hover {
            background: #00c8ff;
            color: black !important;
        }

        /* Alerts like LED boards */
        .stAlert {
            border-radius: 15px;
            border: 2px solid #00c8ff;
            background: rgba(0, 20, 40, 0.85);
            color: #e0e0e0 !important;
        }

        /* Download button: spotlight silver */
        .stDownloadButton>button {
            background: #00c8ff;
            color: black;
            font-weight: bold;
            border-radius: 15px;
            border: 2px solid white;
            box-shadow: 0 0 8px #00c8ff;
        }
        .stDownloadButton>button:hover {
            background: white;
            border-color: #00c8ff;
            color: #003366;
        }
        </style>
    """, unsafe_allow_html=True)




def main():
    st.set_page_config(
        page_title="⚽ Football Video Analysis",
        page_icon="⚽",
        layout="wide"
    )

    # Apply theme
    add_theme()
    
    st.title("⚽ Football Video Analysis App")
    st.markdown("Upload a football video to analyze player tracking, team assignment, and ball detection! 🏟️")
    
    # Load models
    model_path = "models/best.pt"
    tracker = load_tracker(model_path)
    if tracker is None:
        st.error("❌ Failed to load YOLO model from 'models/best.pt'")
        st.error("Please ensure the model file exists at the correct path")
        st.stop()
    
    team_assigner = load_team_assigner()
    if team_assigner is None:
        st.error("❌ Failed to initialize TeamAssigner")
        st.stop()

    player_ball_assigner = load_player_ball_assigner()

    # Sidebar: processing mode selection
    st.sidebar.header("⚡ Processing Mode ⚽")
    mode = st.sidebar.radio(
        "Choose processing quality:",
        ["🚀 Fast", "⚖️ Balanced", "🎯 High Quality"],
        index=0
    )

    if mode == "🚀 Fast":
        # Low res for speed
        max_frames, skip_frames, resize_width, fast_mode = None, 3, 640, True
    elif mode == "⚖️ Balanced":
        # Medium res so annotations appear
        max_frames, skip_frames, resize_width, fast_mode = None, 2, 1280, True
    else:  # 🎯 High Quality
        max_frames, skip_frames, resize_width, fast_mode = None, 1, None, False



    # File uploader
    uploaded_file = st.file_uploader(
        "📂 Choose a football video file", 
        type=['mp4', 'avi', 'mov', 'mkv'],
        help="Upload a football video file for analysis ⚽"
    )
    
    if uploaded_file is not None:
        st.info(f"📁 File: {uploaded_file.name} ({uploaded_file.size / 1024 / 1024:.2f} MB)")
        
        # Show original video
        st.subheader("📹 Original Video")
        st.video(uploaded_file)
        
        with st.spinner("🔄 Processing video... This may take a few minutes ⏳"):
            uploaded_file.seek(0)  # Reset file pointer

            output_frames, tracks = process_video(
                uploaded_file, 
                tracker, 
                team_assigner,
                player_ball_assigner=player_ball_assigner,
                max_frames=max_frames,
                skip_frames=skip_frames,
                resize_width=resize_width,
                fast_mode=fast_mode
            )
                
            st.success("✅ Video analysis completed! 🎉")
            st.info(f"📊 Processed {len(output_frames)} frames")
            
            st.subheader("🎯 Analyzed Video ⚽")
            video_bytes = frames_to_video_bytes(output_frames)
            
            if video_bytes:
                st.success("✅ Video conversion completed! 🏆")
                st.video(video_bytes)
                
                file_base = uploaded_file.name.rsplit('.', 1)[0]
                st.download_button(
                    label="📥 Download Analyzed Video",
                    data=video_bytes,
                    file_name=f"{file_base}_analyzed.mp4",
                    mime="video/mp4"
                )
            else:
                st.error("❌ Failed to generate output video")
                st.warning("📸 Showing sample analyzed frames instead:")
                num_sample_frames = min(10, len(output_frames))
                sample_indices = np.linspace(0, len(output_frames)-1, num_sample_frames, dtype=int)
                for idx in sample_indices:
                    frame_rgb = cv2.cvtColor(output_frames[idx], cv2.COLOR_BGR2RGB)
                    st.image(frame_rgb, caption=f"📸 Frame {idx+1}")
                    
    else:
        st.info("👆 Please upload a football video file to get started! ⚽")
        
        st.subheader("📋 How to use:")
        st.write("1. Choose your preferred processing mode in the sidebar 🖥️")
        st.write("2. Upload a football video file ⚽")
        st.write("3. Wait while the video is analyzed 🔍")
        st.write("4. View results including tracked players, team assignments, and ball detection 🏟️")
        
        st.subheader("⚡ Processing Modes:")
        st.write("- **🚀 Fast**: Quick analysis (~250 frames, reduced quality) - Best for testing")
        st.write("- **⚖️ Balanced**: Good balance of speed and quality (~400 frames)")  
        st.write("- **🎯 High Quality**: Full analysis with maximum quality (slower)")
        
        st.subheader("🎯 What this app does:")
        st.write("- **Player Detection & Tracking**: Identifies and tracks all players throughout the video")
        st.write("- **Team Assignment**: Automatically assigns players to teams based on jersey colors")
        st.write("- **Ball Detection**: Detects and tracks the football")
        st.write("- **Referee Detection**: Identifies referees on the field")
        st.write("- **Visual Annotations**: Adds colored ellipses and IDs to tracked objects")
        
        st.subheader("⚡ Performance:")
        st.write("- **Auto-loaded Models**: YOLO model is automatically loaded and cached")
        st.write("- **Fast Processing**: Optimized video analysis with cached models")
        st.write("- **One-Click Analysis**: Simply upload video and watch the results ⚽")




if __name__ == "__main__":
    main()
