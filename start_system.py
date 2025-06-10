#!/usr/bin/env python3
"""
Climbing Detection System - Auto Launcher
Otomatik olarak Web GUI ve detector'ı başlatır
"""
import subprocess
import threading
import time
import signal
import sys
import webbrowser

def launch_web_gui():
    """Web GUI server'ını başlat"""
    print("🌐 Web GUI Server başlatılıyor...")
    try:
        gui_process = subprocess.Popen(['python3', 'web_server.py'])
        # 3 saniye bekle ve tarayıcıyı aç
        time.sleep(3)
        try:
            print("🌐 Tarayıcı açılıyor: http://localhost:5002")
            webbrowser.open('http://localhost:5002')
        except:
            print("💡 Manuel olarak açın: http://localhost:5002")
        return gui_process
    except Exception as e:
        print(f"❌ Web GUI başlatılamadı: {e}")
        return None

def launch_detector():
    """Climbing detector'ı başlat"""
    print("🎥 Climbing Detector başlatılıyor...")
    time.sleep(4)  # Web GUI'nin başlaması için bekle
    try:
        detector_process = subprocess.Popen(['python3', 'live_detector.py'])
        return detector_process
    except Exception as e:
        print(f"❌ Detector başlatılamadı: {e}")
        return None

def signal_handler(sig, frame):
    """Ctrl+C ile temiz çıkış"""
    print("\n🛑 Sistem kapatılıyor...")
    global gui_process, detector_process
    
    if detector_process:
        detector_process.terminate()
        print("✅ Detector durduruldu")
    
    if gui_process:
        gui_process.terminate()
        print("✅ Web GUI durduruldu")
    
    sys.exit(0)

if __name__ == "__main__":
    print("🚀 Climbing Detection System Başlatılıyor...")
    print("=" * 50)
    
    # Signal handler için
    signal.signal(signal.SIGINT, signal_handler)
    
    # Global process değişkenleri
    gui_process = None
    detector_process = None
    
    try:
        # 1. Web GUI'yi başlat
        gui_process = launch_web_gui()
        if gui_process:
            print("✅ Web GUI başlatıldı")
        else:
            print("❌ Web GUI başlatılamadı, çıkılıyor...")
            sys.exit(1)
        
        # 2. Detector'ı başlat
        detector_process = launch_detector()
        if detector_process:
            print("✅ Detector başlatıldı")
        else:
            print("❌ Detector başlatılamadı")
            if gui_process:
                gui_process.terminate()
            sys.exit(1)
        
        print("\n🎯 Sistem aktif!")
        print("📹 Kamera açık - Climbing detection çalışıyor")
        print("🌐 Web GUI: http://localhost:5002")
        print("📡 Socket Server: Port 5001")
        print("\n💡 Çıkmak için Ctrl+C tuşlarına basın")
        print("=" * 50)
        
        # Process'leri takip et
        while True:
            # GUI process kontrolü
            if gui_process and gui_process.poll() is not None:
                print("⚠️ Web GUI process durdu, yeniden başlatılıyor...")
                gui_process = launch_web_gui()
            
            # Detector process kontrolü
            if detector_process and detector_process.poll() is not None:
                print("⚠️ Detector process durdu, yeniden başlatılıyor...")
                detector_process = launch_detector()
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        signal_handler(None, None)
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        signal_handler(None, None)