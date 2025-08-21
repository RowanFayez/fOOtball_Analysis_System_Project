# ⚽ Football Analysis System using YOLOv5  

This project is a **Computer Vision system for football match analysis**. It combines **YOLOv5** with tracking, clustering, and geometric transformations to detect, track, and analyze players, referees, and the football in real match videos.  

The system goes beyond simple detection — it provides insights such as **ball possession statistics, player speed, and distance covered** by using advanced techniques like **KMeans clustering, optical flow, and perspective transformation**.  

---

## 📌 Key Features  

- **Player, Referee, and Ball Detection**  
  - Uses **YOLOv5**, one of the best object detection models, trained on a custom dataset.  

- **Tracking Across Frames**  
  - Assigns unique IDs to each player, referee, and the ball for consistent tracking.  

- **Team Assignment**  
  - Uses **KMeans clustering** on jersey colors for team classification.  

- **Ball Possession Analysis**  
  - Measures each team’s ball acquisition percentage over the course of a match.  

- **Camera Motion Estimation**  
  - Applies **Optical Flow** to estimate and compensate for camera movement between frames.  

- **Real-World Movement Measurement**  
  - Uses **Perspective Transformation** to convert pixel distances into real-world meters.  

- **Player Speed & Distance**  
  - Calculates each player’s speed and the distance they cover throughout the match.  

---

## 📂 Project Structure  

```
├── models/
│   ├── best.pt                   # YOLOv5 trained weights
│   ├── player_ball_assigner/      # Assigns ball possession to players
│   ├── TeamAssigner/              # Team assignment using jersey colors
│   └── trackers/                  # Object detection & tracking utilities
│
├── training/
│   ├── football-players-detection-1/   # Training dataset
│   └── football_training_yolo_v5.ipynb # Notebook for YOLOv5 training
│
├── utils/                         # Helper functions
├── main.py                        # Entry point for running the system
├── requirements.txt               # Dependencies
└── README.md                      # Documentation
```

---

## ⚙️ Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/football-analysis-yolov5.git
   cd football-analysis-yolov5
   ```

2. Create and activate a virtual environment:  
   ```bash
   python -m venv football
   source football/bin/activate   # Linux/Mac
   football\Scripts\activate      # Windows
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

---

## 📊 Training YOLOv5  

- The model is trained on a custom dataset of **football players, referees, and the ball**.  
- Training is done in `training/football_training_yolo_v5.ipynb`.  
- Output weights are saved in `models/best.pt`.  

---

## ▶️ Usage  

Run the system on a football video:  

```bash
python main.py --video path_to_video.mp4
```

The output will include:  
- Bounding boxes for players, referees, and the ball.  
- Player tracking with unique IDs.  
- Team classification (by jersey color).  
- Ball possession percentage for each team.  


## 🛠️ Technologies & Concepts  

- **YOLOv5** → Object detection (players, referees, ball).  
- **Object Tracking** → ID assignment across frames.  
- **KMeans Clustering** → Team assignment by jersey colors.   
- **Perspective Transformation** → Real-world movement measurement.  
- **Speed & Distance Metrics** → Player performance analysis.


