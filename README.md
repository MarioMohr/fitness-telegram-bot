# 🏋️ Fitness Tracker Telegram Bot

A lightweight, containerized Python Telegram bot deployed on a headless Debian server to track daily fitness activities, swimming pool statistics, nutrition elements, and weight logging.

---

## 📁 Repository Structure

    fitness/                         # Git repository root folder
    ├── app/                         # Main application execution context
    │   ├── bot.py                   # Main Python bot application entry point script
    │   ├── backup.sh                # Automation script for backups, git pushes, and container restarts
    │   └── requirements.txt         # High level pinned third party Python package dependencies
    ├── data/                        # Local state persistence storage directory
    │   └── fitness.db               # Live production SQLite transactional relational database file
    ├── docker-compose.yml           # Production container runtime virtualization orchestration stack
    └── .env                         # Template reference tracking required environment variables

---

## 🚀 Core Features

* **Clean Interactive Interface:** Uses Telegram native keyboard structures to provide a quick custom navigation dashboard.
* **Pool Status Tracking:** Direct monitoring for swimming logs, containing automated target evaluations and status histories.
* **Dynamic Yoga Matrix:** Supports a diverse range of targeted DDP Yoga video modules with a clean button interface.
* **Automatic Schema Adjustments:** Built in checking routines handle column upgrades instantly on launch without data loss.
* **Localized Timezone Handling:** Configured for seamless Asia/Kuala_Lumpur database timestamping.
* **Automated Toolchain Integration:** Custom backup utilities manage service stops, system snapshots, physical device replication, remote git pushes, and automated hot restarts.

---

## 🛠️ Initial System Setup

### 1. Generate Your Telegram Bot Token
1. Open a chat with the official **@BotFather** account inside Telegram.
2. Send the command: `/newbot`
3. Follow the prompt instructions to assign a descriptive name and a unique username ending in `_bot`.
4. Copy the secure, randomized alphanumerical token string provided. This string links your script to the Telegram API.

### 2. Configure Your Environment File
Create a file named exactly `.env` directly inside your main folder ('fitness/'). Add your copied token string without using any surrounding quotes:

    TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE

---

## 📦 Host Operating System Engine Installations

Run the respective package manager commands on your server to install Docker and the Docker Compose plugin:

### Debian / Ubuntu Linux
    sudo apt update
    sudo apt install -y docker-compose-plugin docker.io sqlite3
    sudo systemctl enable --now docker

### Arch Linux
    sudo pacman -Syu --needed docker docker-compose sqlite
    sudo systemctl enable --now docker

### Gentoo Linux
    sudo emerge --ask --verbose app-containers/docker app-containers/docker-compose dev-db/sqlite
    sudo rc-update add docker default
    sudo rc-service docker start

---

## 💾 Database Layer Management

The `fitness.db` file is managed dynamically by the application layer:
* **Automatic Initialization:** You do not need to manually create any tables, columns, or files beforehand. On the very first launch, the initialization methods instantly structure the file from scratch inside your bound storage mount folder.
* **Automatic Migrations:** Structural runtime columns (such as schema updates for tracking specific yoga videos or cardiorespiratory cardio metrics) check for existence and patch themselves gracefully without triggering database exceptions or altering data history.

---

## ⚙️ Standard Production Lifecycle Actions

### Run the Bot Without Backups
To launch the service stack, build your image layer, and execute the polling process safely in the background without invoking external bash distributions or remote code additions:

    cd /home/mario/fitness
    docker compose up -d --build

### Stop the Bot Safely
To halt the execution context and release host network bindings without deleting persistent databases:

    cd /home/mario/fitness
    docker compose down

### View Live Execution Logs
To inspect application logs or debug active communication threads:

    cd /home/mario/fitness
    docker compose logs -f fitness_trainer

---

## 🛡️ Automated Backups, Git Upgrades, and Hot Restarts

The provided `app/backup.sh` deployment script allows you to perform structural updates safely.

### 1. Tailor Your Backup Storage Locations
Open `app/backup.sh` in your editor and adjust the global system location strings to match your server mounts:

    REPO_DIR="/home/mario/fitness"
    APP_DIR="/home/mario/fitness/app"
    SAMBA_DIR="/mnt/media/backups/docker"  # Target storage share folder path
    USB_DIR="/mnt/MiniUSB/docker"          # Local physical flash drive mount path

### 2. Run the Automation Routine
Make sure the script has execution rights on your filesystem:

    chmod +x /home/mario/fitness/app/backup.sh

Execute it whenever you want to commit code alterations, back up metrics, or trigger safe container updates:

    /home/mario/fitness/app/backup.sh

**What the script handles in sequence:**
1. Collects a quick manual change description text for your Git log.
2. Stops the `fitness_trainer` container cleanly to freeze any database operations.
3. Packages the whole code structure into a timestamped, compressed archive (`.tar.gz`), ignoring massive invisible `.git/` histories.
4. Delivers duplicate copies of that archive directly to your Samba Share network paths and local USB flash drives if they are connected.
5. Pushes all local code updates cleanly to your remote GitHub repository branch.
6. Automatically rebuilds the container layer from your source file and fires the container back up into an active running state.

