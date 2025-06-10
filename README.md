# 🧗‍♂️ Real-Time Climbing Detection System

A hybrid Docker-based system that uses YOLO pose estimation to detect climbing movements in real-time through webcam feed. The system provides instant notifications through a modern web-based GUI interface and stores detection events in a MySQL database.

## 🎯 Features

- **Real-time Climbing Detection**: Uses YOLOv8 pose estimation to analyze knee angles and detect climbing movements
- **Live Camera Feed**: Direct webcam access for real-time monitoring
- **Web-based GUI**: Modern browser-based alert system with real-time logging and WebSocket integration
- **Real-time Notifications**: Instant alerts displayed in web interface with live updates
- **Database Storage**: MySQL database for storing detection events and statistics
- **Hybrid Architecture**: Optimized for macOS with host-based detection and containerized services
- **Auto-launcher**: Single command to start the entire system
- **Configurable Detection**: Adjustable sensitivity and detection parameters

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Host System   │    │   Web GUI       │    │  Docker MySQL   │
│                 │    │   (Port 5002)   │    │   (Port 3307)   │
│ • Webcam Access │───▶│ • Web Interface │◄───│ • Event Storage │
│ • YOLO Model    │    │ • Real-time Log │    │ • Statistics    │
│ • Detection     │    │ • WebSocket     │    │ • Data Persist  │
│                 │    │ • Socket Server │    │                 │
│                 │    │   (Port 5001)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **macOS** (tested on macOS Monterey+)
- **Docker Desktop** installed and running
- **Python 3.9+** with pip
- **Webcam** access permissions
- **8GB+ RAM** recommended for YOLO model
- **Modern web browser** (Chrome, Firefox, Safari)

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

5. **Open Web GUI**
```bash
# Web interface will automatically open at:
# http://localhost:5002
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
├── climbing_server.py      # Web GUI server with WebSocket
├── climbing_client.py      # Communication client
├── alert_utils.py          # Database and email utilities
└── controller.py           # Legacy controller (deprecated)
```

## ⚙️ Configuration

### Web GUI Configuration

Edit `climbing_server.py` to customize web interface:

```python
# Web server settings
WEB_HOST = '127.0.0.1'       # Web interface host
WEB_PORT = 5002              # Web interface port
SOCKET_PORT = 5001           # Internal socket port
MESSAGE_LIMIT = 100          # Maximum messages to display
```

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

### Accessing the Web Interface

1. **Open your web browser**
2. **Navigate to**: `http://localhost:5002`
3. **Monitor real-time alerts** in the web interface
4. **View live connection status** (🟢 Connected / 🔴 Disconnected)

### Web Interface Features

- **Real-time Alert Display**: Live climbing detection notifications
- **Message History**: Last 100 detection events with timestamps
- **Connection Status**: Visual indicator of system connectivity
- **Auto-scroll**: Automatic scrolling to latest messages
- **Dark Theme**: Modern dark interface for better visibility

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

- **Web Interface**: Real-time alerts at `http://localhost:5002`
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

#### 2. Web Interface Not Loading

**Problem**: Cannot access `http://localhost:5002`

**Solutions**:
```bash
# Check if web server is running
ps aux | grep climbing_server

# Check port availability
lsof -i :5002
lsof -i :5001

# Restart web server
pkill -f climbing_server
python3 climbing_server.py
```

#### 3. WebSocket Connection Issues

**Problem**: Web interface shows "🔴 Bağlantı Kesildi"

**Solution**:
```bash
# Check socket server status
netstat -an | grep 5001

# Restart the climbing server
pkill -f climbing_server
python3 climbing_server.py
```

#### 4. Port Already in Use

**Problem**: `OSError: [Errno 48] Address already in use`

**Solutions**:
```bash
# Check what's using the ports
lsof -i :5001  # Socket server
lsof -i :5002  # Web interface
lsof -i :3307  # MySQL

# Kill conflicting processes
docker-compose down
pkill -f "python3 climbing_server.py"

# Or change ports in configuration files
```

#### 5. Docker Connection Issues

**Problem**: `Cannot connect to Docker daemon`

**Solution**:
```bash
# Ensure Docker Desktop is running
open -a Docker

# Verify Docker is running
docker ps
```

#### 6. YOLO Model Download Issues

**Problem**: Model fails to download or load

**Solution**:
```bash
# Check internet connection
# Manually download model
python3 -c "from ultralytics import YOLO; YOLO('yolov8m-pose.pt')"

# Clear cache if corrupted
rm -rf ~/.cache/ultralytics/
```

#### 7. MySQL Connection Failed

**Problem**: `[DB Error] Can't connect to MySQL server`

**Solution**:
```bash
# Check container status
docker ps
docker logs climbing_mysql

# Restart MySQL container
docker-compose restart mysql

# Verify port configuration
lsof -i :3307
```

#### 8. Web Interface Not Updating

**Problem**: Detection works but web interface doesn't show alerts

**Solution**:
```bash
# Check Flask-SocketIO installation
pip3 install flask-socketio

# Verify socket communication
python3 -c "import socket; s=socket.socket(); s.connect(('127.0.0.1', 5001)); print('Socket OK')"

# Check browser console for WebSocket errors
# Open browser dev tools → Console tab
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

#### Web Interface Slow
```bash
# Reduce message history
# Edit climbing_server.py:
MESSAGE_LIMIT = 50  # Reduce from 100

# Clear browser cache
# Hard refresh: Cmd+Shift+R (macOS)
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

### Test Web Interface
```bash
# Start only web server
python3 climbing_server.py
# Open http://localhost:5002 in browser
```

### Test WebSocket Connection
```bash
# Check WebSocket in browser console:
# Open http://localhost:5002
# Press F12 → Console
# Look for WebSocket connection messages
```

### Test Detection Manually
```bash
# Run detector only
python3 live_detector.py
# Perform climbing movements in front of camera
# Check web interface for alerts
```

## 📊 System Requirements

### Minimum Requirements
- **OS**: macOS 10.15+
- **RAM**: 4GB
- **CPU**: Dual-core 2.0GHz
- **Storage**: 2GB free space
- **Camera**: Built-in or USB webcam
- **Browser**: Chrome 60+, Firefox 55+, Safari 12+

### Recommended Requirements
- **OS**: macOS 12.0+
- **RAM**: 8GB+
- **CPU**: Quad-core 2.5GHz+
- **Storage**: 5GB free space
- **Camera**: HD webcam (1080p)
- **Browser**: Latest Chrome, Firefox, or Safari

## 🌐 Web Interface Details

### Features
- **Real-time Updates**: WebSocket-based live alert system
- **Message History**: Displays last 100 detection events
- **Timestamps**: Each alert includes precise time information
- **Connection Status**: Visual indicator of system health
- **Responsive Design**: Works on desktop and mobile browsers
- **Dark Theme**: Professional dark interface

### Ports Used
- **5002**: Web interface (HTTP)
- **5001**: Internal socket server
- **3307**: MySQL database

### Browser Compatibility
- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+

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
2. **Review logs**: 
   - Container logs: `docker logs climbing_mysql`
   - Web server logs: Check terminal running `climbing_server.py`
   - Browser console: Press F12 in web interface
3. **Open an issue** on GitHub with:
   - Your macOS version
   - Browser version
   - Error messages
   - Steps to reproduce
   - Log outputs

## 🏷️ Version

**Current Version**: 2.0.0

### Recent Updates
- 🌐 **Web-based GUI**: Modern browser interface replacing desktop notifications
- 🔄 **WebSocket Integration**: Real-time updates without page refresh
- 📱 **Responsive Design**: Works on desktop and mobile browsers
- 🎨 **Dark Theme Interface**: Professional dark mode for better visibility
- 📊 **Message History**: View last 100 detection events with timestamps
- 🟢 **Connection Status**: Visual indicator of system health
- ⚡ **Improved Performance**: Optimized web server with Flask-SocketIO

### Previous Versions
- ✅ v1.0.0: Hybrid architecture for optimal macOS compatibility
- ✅ v1.0.0: Auto-launcher system
- ✅ v1.0.0: Improved error handling and logging
- ✅ v1.0.0: Docker containerization for services

## 🙏 Acknowledgments

- **Ultralytics YOLO** for pose estimation
- **OpenCV** for computer vision
- **Flask & Flask-SocketIO** for web interface
- **Docker** for containerization
- **MySQL** for database storage
