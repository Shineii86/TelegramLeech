# Copyright 2025 © Shinei Nouzen | https://github.com/Shineii86
# Licensed under the MIT License
# Professional Colab Leech Implementation

# ==================== CONFIGURATION ====================
API_ID = 0  # @param {type: "integer"}
API_HASH = ""  # @param {type: "string"}
BOT_TOKEN = ""  # @param {type: "string"}
USER_ID = 0  # @param {type: "integer"}
DUMP_ID = 0  # @param {type: "integer"}
# =======================================================

import subprocess
import time
import json
import shutil
import os
import sys
from IPython.display import clear_output
from threading import Thread, Event
from typing import Dict, Any

class ColabLeechSetup:
    """
    Professional setup class for Telegram Leech Bot on Google Colab
    """
    
    def __init__(self, api_id: int, api_hash: str, bot_token: str, user_id: int, dump_id: int):
        self.credentials = {
            "API_ID": api_id,
            "API_HASH": api_hash,
            "BOT_TOKEN": bot_token,
            "USER_ID": user_id,
            "DUMP_ID": self._validate_dump_id(dump_id)
        }
        self.working = Event()
        self.working.set()
        
        # Constants
        self.REPO_URL = "https://github.com/Shineii86/TelegramLeech"
        self.REPO_PATH = "/content/TelegramLeech"
        self.CREDENTIALS_PATH = f"{self.REPO_PATH}/credentials.json"
        self.SESSION_FILE = f"{self.REPO_PATH}/my_bot.session"

    def _validate_dump_id(self, dump_id: int) -> int:
        """Validate and format DUMP_ID"""
        dump_str = str(dump_id)
        if len(dump_str) == 10 and not dump_str.startswith("-100"):
            return int(f"-100{dump_str}")
        return dump_id

    def display_banner(self):
        """Display professional banner"""
        banner = """
╔═══════════════════════════════════════════════╗
║                         TELEGRAM LEECH BOT SETUP                             ║
║                        TelegramLeech Edition v2.0                            ║
║                                                                              ║
║            GitHub: https://github.com/Shineii86/TelegramLeech                ║
║              Copyright © Shinei Nouzen All Rights Reserved                   ║
╚═══════════════════════════════════════════════╝
        """
        print(banner)

    def loading_animation(self):
        """Professional loading animation"""
        animation_chars = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        i = 0
        while self.working.is_set():
            print(f"\r🔄 Setting up environment {animation_chars[i % len(animation_chars)]}", end="")
            i += 1
            time.sleep(0.2)
        clear_output()

    def run_command(self, command: str, description: str) -> bool:
        """Execute shell command with error handling"""
        try:
            print(f"📦 {description}...")
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=300  # 5 minute timeout
            )
            if result.returncode != 0:
                print(f"❌ Error in {description}: {result.stderr}")
                return False
            print(f"✅ {description} completed successfully")
            return True
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout during {description}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during {description}: {str(e)}")
            return False

    def cleanup_environment(self):
        """Clean up previous installations"""
        print("🧹 Cleaning up environment...")
        
        # Remove sample data if exists
        if os.path.exists("/content/sample_data"):
            shutil.rmtree("/content/sample_data")
            print("✅ Removed sample data")
        
        # Remove previous repository
        if os.path.exists(self.REPO_PATH):
            shutil.rmtree(self.REPO_PATH)
            print("✅ Removed previous installation")
        
        # Remove previous session file
        if os.path.exists(self.SESSION_FILE):
            os.remove(self.SESSION_FILE)
            print("✅ Removed previous session file")

    def setup_repository(self) -> bool:
        """Clone and setup the repository"""
        commands = [
            (f"git clone {self.REPO_URL}", "Cloning repository"),
            (f"bash {self.REPO_PATH}/setup.sh", "Running setup script"),
            ("apt update && apt install -y ffmpeg aria2", "Installing system dependencies"),
            (f"pip3 install -r {self.REPO_PATH}/requirements.txt", "Installing Python dependencies")
        ]
        
        for command, description in commands:
            if not self.run_command(command, description):
                return False
        return True

    def save_credentials(self):
        """Save credentials to JSON file"""
        try:
            with open(self.CREDENTIALS_PATH, 'w') as file:
                json.dump(self.credentials, file, indent=4)
            print("✅ Credentials saved successfully")
            
            # Verify the file was written correctly
            with open(self.CREDENTIALS_PATH, 'r') as file:
                saved_data = json.load(file)
            if saved_data == self.credentials:
                print("✅ Credentials verified")
            else:
                print("⚠️  Credentials verification failed")
                
        except Exception as e:
            print(f"❌ Failed to save credentials: {str(e)}")
            raise

    def start_bot(self):
        """Start the leech bot"""
        print("\n🎉 Setup completed successfully!")
        print("🚀 Starting Telegram Leech Bot...")
        
        try:
            # Change to repository directory and start the bot
            os.chdir(self.REPO_PATH)
            subprocess.run(["python3", "-m", "colab_leecher"])
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
        except Exception as e:
            print(f"❌ Error starting bot: {str(e)}")

    def setup(self):
        """Main setup method"""
        try:
            self.display_banner()
            
            # Validate credentials
            if not all([self.credentials["API_ID"], self.credentials["API_HASH"], 
                       self.credentials["BOT_TOKEN"], self.credentials["USER_ID"]]):
                print("❌ Please fill in all required credentials")
                return False

            # Start loading animation
            loader_thread = Thread(target=self.loading_animation)
            loader_thread.daemon = True
            loader_thread.start()

            # Perform setup steps
            self.cleanup_environment()
            
            if not self.setup_repository():
                return False
                
            self.save_credentials()
            
            # Stop loading animation
            self.working.clear()
            loader_thread.join(timeout=1)
            
            # Start the bot
            self.start_bot()
            return True
            
        except Exception as e:
            self.working.clear()
            print(f"❌ Setup failed: {str(e)}")
            return False

def main():
    """Main execution function"""
    try:
        # Initialize and run setup
        leech_setup = ColabLeechSetup(
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            user_id=USER_ID,
            dump_id=DUMP_ID
        )
        
        success = leech_setup.setup()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
