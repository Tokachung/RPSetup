# 🖥️ Remotely Connecting to and Running a Camera Stream on Raspberry Pi

This guide explains how to connect to your Raspberry Pi remotely via SSH using VS Code, and how to run a Python camera stream using `picamera2` and `opencv`.

---

## 🔗 1. Connect to Raspberry Pi via SSH (VS Code or Terminal)

### Step 1: Install the Remote-SSH Extension
- In VS Code, open the Extensions tab (`Ctrl + Shift + X`).
- Search for and install **“Remote - SSH”** by Microsoft.

### Step 2: Add Your Raspberry Pi as a Host
- Open the Command Palette (`Ctrl + Shift + P`) → **Remote-SSH: Add New SSH Host**.
- Enter the following (update values as needed):
  ```bash
  Host <your-pi-alias>
    HostName <your-pi-ip-address>
    User <your-username>
  ```
  **Example:**
  ```bash
  Host mypi
    HostName 192.168.4.57
    User pi
  ```
  - `Host` → a short nickname for your device (you’ll use this to connect later).  
  - `HostName` → the Pi’s IP address on your local network.  
  - `User` → the login name you set during setup (default is `pi`, but if you used Raspberry Pi Imager, it’s whatever you created).

### Step 3: Connect from VS Code
- Open the Command Palette again → **Remote-SSH: Connect to Host** → choose the alias you just added.

### Step 4: (Optional) Connect from the Terminal
You can also connect manually:
```bash
ssh <your-username>@<your-pi-ip-address>
```
**Example:**
```bash
ssh pi@192.168.4.57
```
Enter your password when prompted.

---

## ✅ Notes on SSH
- Once connected, your terminal prompt will look like:
  ```bash
  <username>@<hostname>:~ $
  ```
  **Example:**
  ```bash
  pi@raspberrypi:~ $
  ```
- You can set up **SSH key authentication** to skip password prompts.
- If you used Raspberry Pi Imager, your username and hostname are whatever you entered in the setup options.

---

## 📷 2. Set Up and Run the Camera Stream

### Step 1: Install dependencies
Run the following commands on your Raspberry Pi:
```bash
sudo apt update
sudo apt install -y python3-picamera2
sudo apt install -y python3-opencv
```

### Step 2: Run the stream script
Execute your Python script:
```bash
python3 stream.py
```

---

## ✅ Notes on Camera Streaming
- Ensure your camera is **connected and enabled**:
  ```bash
  sudo raspi-config
  ```
  Go to **Interface Options → Camera → Enable**, then reboot.
- If you get an error like `ImportError: No module named picamera2`, confirm you’re using **Raspberry Pi OS Bookworm or later** — `picamera2` isn’t supported on older versions.
- Depending on your script, the video may open in an OpenCV window or broadcast via HTTP (e.g. `http://<pi-ip>:8080`).

---

### 🧩 Optional Improvements
- Set up SSH keys for passwordless login:
  ```bash
  ssh-keygen -t ed25519
  ssh-copy-id <your-username>@<your-pi-ip-address>
  ```
- Add a static IP in your router so your Pi’s address doesn’t change.
- Use VS Code’s integrated terminal to run and debug scripts directly on the Pi.

### Useful Resources
- https://github.com/raspberrypi/picamera2