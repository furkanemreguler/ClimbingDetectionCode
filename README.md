# 🧗‍♂️ Real-Time Climbing Detection System

A hybrid Docker-based system that uses YOLO pose estimation to detect climbing movements in real-time through webcam feed. The system provides instant notifications through a GUI interface and stores detection events in a MySQL database.

## 🎯 Features

- **Real-time Climbing Detection**: Uses YOLOv8 pose estimation to analyze knee angles and detect climbing movements
- **Live Camera Feed**: Direct webcam access for real-time monitoring
- **Instant Notifications**: GUI-based alert system with real-time logging
- **Database Storage**: MySQL database for storing detection events and statistics
- **Hybrid Architecture**: Optimized for macOS with host-based detection and containerized services
- **Auto-launcher**: Single command to start the entire system
- **Configurable Detection**: Adjustable sensitivity and detection parameters

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Host System   │    │   GUI Server    │    │  Docker MySQL   │
│                 │    │   (Port 5001)   │    │   (Port 3307)   │
│ • Webcam Access │───▶│ • Alert Display │◄───│ • Event Storage │
│ • YOLO Model    │    │ • Real-time Log │    │ • Statistics    │
│ • Detection     │    │ • Notifications │    │ • Data Persist  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **macOS** (tested on macOS Monterey+)
- **Docker Desktop** installed and running
- **Python 3.9+** with pip
- **Webcam** access permissions
- **8GB+ RAM** recommended for YOLO model

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/climbing-detection-system.git
cd climbing-detection-system
```

2. **Install Python dependencies**
```bash
pip3 install torch torchvision ultralytics opencv-python numpy mysql-connector-python flask flask-socketio
```

3. **Start Docker containers**
```bash
docker-compose up -d
```

4. **Launch the complete system**
```bash
python3 start_system.py
```

## 📁 Project Structure

```
climbing-detection-system/
├── README.md                 # This file
├── docker-compose.yml        # Docker services configuration
├── Dockerfile               # Docker image definition
├── requirements.txt         # Python dependencies
├── start_system.py         # Auto-launcher script
├── live_detector.py        # Main detection engine
├── climbing_server.py      # GUI notification server
├── climbing_client.py      # Communication client
├── alert_utils.py          # Database and email utilities
└── controller.py           # Legacy controller (deprecated)
```

## ⚙️ Configuration

### Detection Parameters

Edit `live_detector.py` to customize detection behavior:

```python
# Detection sensitivity
BENT_THRESHOLD = 5          # Frames required for detection
KNEE_MIN, KNEE_MAX = 45, 130  # Knee angle range for climbing
CONF_THRESH = 0.30          # YOLO confidence threshold
WINDOW = 15                 # Detection window size
```

### Database Configuration

Modify `alert_utils.py` for database settings:

```python
MYSQL_CONFIG = {
    "host": "127.0.0.1",     # Database host
    "port": 3307,            # Database port
    "user": "climbing_project",
    "password": "smartcampus",
    "database": "climbing_system"
}
```

### Email Notifications

Configure email alerts in `alert_utils.py`:

```python
SECURITY_EMAIL = "security-team@example.com"
SENDER_EMAIL   = "youremail@gmail.com"
SENDER_PASS    = "your_app_password"
```

## 🖥️ Usage

### Starting the System

```bash
# Option 1: Auto-launcher (Recommended)
python3 start_system.py

# Option 2: Manual startup
docker-compose up -d
python3 climbing_server.py &
python3 live_detector.py
```

### Stopping the System

```bash
# If using auto-launcher
Ctrl+C

# If manual startup
docker-compose down
pkill -f "python3 climbing_server.py"
pkill -f "python3 live_detector.py"
```

### Monitoring

- **GUI Interface**: Automatic popup window showing real-time alerts
- **Terminal Logs**: Detection events logged in the terminal
- **Database**: Events stored in MySQL for historical analysis

## 🔧 Troubleshooting

### Common Issues

#### 1. Camera Access Denied

**Problem**: `OpenCV: not authorized to capture video (status 0)`

**Solution**:
```bash
# Grant camera permissions to Terminal
# macOS Settings → Privacy & Security → Camera → Terminal ✅
```

#### 2. Port Already in Use

**Problem**: `OSError: [Errno 48] Address already in use`

**Solutions**:
```bash
# Check what's using the port
lsof -i :5001
lsof -i :3307

# Kill conflicting processes
docker-compose down
pkill -f "python3 climbing_server.py"

# Or change ports in configuration files
```

#### 3. Docker Connection Issues

**Problem**: `Cannot connect to Docker daemon`

**Solution**:
```bash
# Ensure Docker Desktop is running
open -a Docker

# Verify Docker is running
docker ps
```

#### 4. YOLO Model Download Issues

**Problem**: Model fails to download or load

**Solution**:
```bash
# Check internet connection
# Manually download model
python3 -c "from ultralytics import YOLO; YOLO('yolov8m-pose.pt')"

# Clear cache if corrupted
rm -rf ~/.cache/ultralytics/
```

#### 5. MySQL Connection Failed

**Problem**: `[DB Error] Can't connect to MySQL server`

**Solution**:
```bash
# Check container status
docker ps
docker logs climbing_mysql

# Restart MySQL container
docker-compose restart mysql

# Verify port configuration
# Check if port 3307 is available
lsof -i :3307
```

#### 6. GUI Not Appearing

**Problem**: Detection works but no GUI window

**Solution**:
```bash
# Check if Tkinter is installed
python3 -c "import tkinter"

# Install Tkinter if missing (macOS)
brew install python-tk

# Check GUI process
ps aux | grep climbing_server
```

### Performance Issues

#### High CPU Usage
```bash
# Reduce detection frequency
# Edit live_detector.py:
FPS = 10  # Reduce from 15
QUEUE_SIZE = 1  # Keep minimal
```

#### High Memory Usage
```bash
# Monitor memory
docker stats
top -p $(pgrep -f live_detector)

# Restart system if memory leaks
python3 start_system.py
```

## 🧪 Testing

### Test Camera Access
```bash
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK:', cap.isOpened()); cap.release()"
```

### Test Database Connection
```bash
python3 -c "from alert_utils import init_db; init_db()"
```

### Test Detection Manually
```bash
# Run detector only
python3 live_detector.py
# Perform climbing movements in front of camera
```

## 📊 System Requirements

### Minimum Requirements
- **OS**: macOS 10.15+
- **RAM**: 4GB
- **CPU**: Dual-core 2.0GHz
- **Storage**: 2GB free space
- **Camera**: Built-in or USB webcam

### Recommended Requirements
- **OS**: macOS 12.0+
- **RAM**: 8GB+
- **CPU**: Quad-core 2.5GHz+
- **Storage**: 5GB free space
- **Camera**: HD webcam (1080p)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter issues not covered in this README:

1. **Check the troubleshooting section** above
2. **Review container logs**: `docker logs climbing_mysql` and `docker logs climbing_server`
3. **Open an issue** on GitHub with:
   - Your macOS version
   - Error messages
   - Steps to reproduce
   - Log outputs

## 🏷️ Version

**Current Version**: 1.0.0

### Recent Updates
- ✅ Hybrid architecture for optimal macOS compatibility
- ✅ Auto-launcher system
- ✅ Improved error handling and logging
- ✅ Docker containerization for services
- ✅ Real-time GUI notifications

## 🙏 Acknowledgments

- **Ultralytics YOLO** for pose estimation
- **OpenCV** for computer vision
- **Docker** for containerization
- **MySQL** for database storage
