# Step-by-Step Guide: Running Shopify AI Analytics in IntelliJ IDEA

## 📋 Complete Beginner-Friendly Guide

---

## PART 1: PREREQUISITES (30 minutes)

### Step 1: Install IntelliJ IDEA Ultimate

1. Go to https://www.jetbrains.com/idea/download/
2. Download **IntelliJ IDEA Ultimate** (NOT Community Edition)
3. Run the installer
4. Follow installation wizard
5. Launch IntelliJ IDEA

**Why Ultimate?** Community Edition doesn't have full Ruby/Rails support.

---

### Step 2: Install Ruby

**On Mac:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Ruby
brew install ruby@3.2

# Verify installation
ruby --version
# Should show: ruby 3.2.x
```

**On Windows:**
1. Download RubyInstaller from https://rubyinstaller.org/
2. Download **Ruby+Devkit 3.2.x (x64)**
3. Run installer, check "Add Ruby to PATH"
4. Open Command Prompt and verify:
```cmd
ruby --version
```

**On Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ruby-full
ruby --version
```

---

### Step 3: Install Python

**On Mac:**
```bash
brew install python@3.11
python3 --version
# Should show: Python 3.11.x
```

**On Windows:**
1. Go to https://www.python.org/downloads/
2. Download Python 3.11.x
3. Run installer
4. **IMPORTANT:** Check "Add Python to PATH"
5. Verify in Command Prompt:
```cmd
python --version
```

**On Linux:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
python3 --version
```

---

### Step 4: Install PostgreSQL

**On Mac:**
```bash
brew install postgresql@14
brew services start postgresql@14

# Verify
psql --version
```

**On Windows:**
1. Download from https://www.postgresql.org/download/windows/
2. Run installer (remember the password you set!)
3. Default port: 5432
4. Verify in Command Prompt:
```cmd
psql --version
```

**On Linux:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

---

### Step 5: Install Redis

**On Mac:**
```bash
brew install redis
brew services start redis

# Verify
redis-cli ping
# Should return: PONG
```

**On Windows:**
1. Download from https://github.com/microsoftarchive/redis/releases
2. Download Redis-x64-3.0.504.msi
3. Run installer
4. Start Redis service from Services app

**On Linux:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

---

## PART 2: PROJECT SETUP (20 minutes)

### Step 6: Clone the Repository

1. Open Terminal (or Command Prompt)
2. Navigate to where you want the project:
```bash
cd ~/Documents  # or C:\Users\YourName\Documents on Windows
```

3. Clone the repository:
```bash
git clone https://github.com/Amansingh80/shopify-ai-analytics.git
cd shopify-ai-analytics
```

**You should now see:**
```
shopify-ai-analytics/
├── rails-api/
├── python-agent/
├── docs/
├── docker-compose.yml
└── README.md
```

---

### Step 7: Open Project in IntelliJ IDEA

1. Launch IntelliJ IDEA
2. Click **"Open"** on the welcome screen
   - OR: `File` → `Open` if already in a project
3. Navigate to the `shopify-ai-analytics` folder
4. Click **"OK"**
5. Wait for IntelliJ to index the project (progress bar at bottom)

**First time?** IntelliJ may ask to trust the project → Click **"Trust Project"**

---

### Step 8: Install IntelliJ Plugins

1. Go to `File` → `Settings` (Windows/Linux) or `IntelliJ IDEA` → `Preferences` (Mac)
2. Click **"Plugins"** in the left sidebar
3. Click **"Marketplace"** tab
4. Search and install these plugins one by one:

   **Plugin 1: Ruby**
   - Search: "Ruby"
   - Find: "Ruby" by JetBrains
   - Click **"Install"**

   **Plugin 2: Python**
   - Search: "Python"
   - Find: "Python" by JetBrains
   - Click **"Install"**

   **Plugin 3: Database Tools** (usually pre-installed)
   - Search: "Database"
   - Should show "Installed"

5. Click **"OK"**
6. **Restart IntelliJ IDEA** when prompted

---

## PART 3: CONFIGURE RUBY (10 minutes)

### Step 9: Add Ruby SDK to IntelliJ

1. Go to `File` → `Project Structure` (or press `Ctrl+Alt+Shift+S`)
2. Click **"SDKs"** in the left panel under "Platform Settings"
3. Click the **"+"** button at the top
4. Select **"Add Ruby SDK"**
5. Choose **"New local..."**
6. Navigate to your Ruby installation:
   - **Mac:** `/usr/local/opt/ruby@3.2/bin/ruby` or `/opt/homebrew/opt/ruby/bin/ruby`
   - **Windows:** `C:\Ruby32-x64\bin\ruby.exe`
   - **Linux:** `/usr/bin/ruby`
7. Click **"OK"**
8. Click **"Apply"** and **"OK"**

---

### Step 10: Mark Rails Directory as Source

1. In the **Project** panel (left side), find the `rails-api` folder
2. Right-click on `rails-api`
3. Select **"Mark Directory as"** → **"Sources Root"**
4. The folder icon should turn blue

---

### Step 11: Install Rails Dependencies

1. Open **Terminal** in IntelliJ:
   - Click `View` → `Tool Windows` → `Terminal`
   - OR: Press `Alt+F12` (Windows/Linux) or `Option+F12` (Mac)

2. Navigate to rails-api:
```bash
cd rails-api
```

3. Install Bundler (if not installed):
```bash
gem install bundler
```

4. Install dependencies:
```bash
bundle install
```

**This will take 2-5 minutes.** You'll see lots of "Installing..." messages.

**If you see errors:**
- Mac: `xcode-select --install` (installs build tools)
- Windows: Make sure Ruby DevKit is installed
- Linux: `sudo apt install build-essential`

---

## PART 4: CONFIGURE PYTHON (10 minutes)

### Step 12: Add Python SDK to IntelliJ

1. Go to `File` → `Project Structure`
2. Click **"SDKs"** in the left panel
3. Click the **"+"** button
4. Select **"Add Python SDK"**
5. Choose **"Virtualenv Environment"**
6. Select **"New environment"**
7. Configure:
   - **Location:** `[your-project-path]/python-agent/venv`
   - **Base interpreter:** Select your Python 3.11 installation
     - Mac: `/usr/local/bin/python3.11` or `/opt/homebrew/bin/python3.11`
     - Windows: `C:\Python311\python.exe`
     - Linux: `/usr/bin/python3.11`
8. Check **"Inherit global site-packages"** (optional)
9. Click **"OK"**
10. Click **"Apply"** and **"OK"**

---

### Step 13: Mark Python Directory as Source

1. In the **Project** panel, find the `python-agent` folder
2. Right-click on `python-agent`
3. Select **"Mark Directory as"** → **"Sources Root"**
4. The folder icon should turn blue

---

### Step 14: Install Python Dependencies

1. In IntelliJ Terminal, navigate to python-agent:
```bash
cd ../python-agent  # if you're still in rails-api
# OR
cd python-agent     # if you're in project root
```

2. Activate virtual environment:

**On Mac/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```cmd
venv\Scripts\activate
```

**You should see `(venv)` at the start of your terminal prompt.**

3. Upgrade pip:
```bash
pip install --upgrade pip
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

**This will take 3-5 minutes.** You'll see lots of "Collecting..." and "Installing..." messages.

---

## PART 5: ENVIRONMENT CONFIGURATION (10 minutes)

### Step 15: Configure Rails Environment

1. In IntelliJ Terminal, go to project root:
```bash
cd ..  # if you're in python-agent
```

2. Copy the Rails environment template:
```bash
cp rails-api/.env.example rails-api/.env
```

3. Open the file in IntelliJ:
   - In Project panel, navigate to `rails-api/.env`
   - Double-click to open

4. Edit the file (replace placeholder values):

```env
# Shopify credentials (we'll add these later)
SHOPIFY_API_KEY=your_shopify_api_key_here
SHOPIFY_API_SECRET=your_shopify_api_secret_here

# Python agent URL (keep as is)
PYTHON_AGENT_URL=http://localhost:8000

# Database (update if your PostgreSQL has different credentials)
DATABASE_URL=postgresql://postgres:postgres@localhost/shopify_analytics_development

# Redis (keep as is)
REDIS_URL=redis://localhost:6379/0

# Rails Secret (we'll generate this next)
SECRET_KEY_BASE=TEMPORARY

# Rails Environment (keep as is)
RAILS_ENV=development
RAILS_LOG_LEVEL=debug
```

5. Generate Rails secret key:
```bash
cd rails-api
bundle exec rails secret
```

6. Copy the long string that appears
7. Replace `TEMPORARY` in `.env` with this string
8. Save the file (`Ctrl+S` or `Cmd+S`)

---

### Step 16: Configure Python Environment

1. Copy the Python environment template:
```bash
cd ..  # back to project root
cp python-agent/.env.example python-agent/.env
```

2. Open `python-agent/.env` in IntelliJ

3. Edit the file:

```env
# OpenAI API Key (we'll add this later)
OPENAI_API_KEY=your_openai_api_key_here

# Shopify API version (keep as is)
SHOPIFY_API_VERSION=2024-01

# Redis (keep as is)
REDIS_URL=redis://localhost:6379/1

# Logging (keep as is)
LOG_LEVEL=INFO
```

4. Save the file

**Note:** We'll add real API keys later. For now, leave the placeholder values.

---

## PART 6: DATABASE SETUP (5 minutes)

### Step 17: Create PostgreSQL Database

1. Make sure PostgreSQL is running:
```bash
# Check if running
psql --version

# If not running, start it:
# Mac:
brew services start postgresql@14

# Linux:
sudo systemctl start postgresql

# Windows: Start from Services app or pgAdmin
```

2. In IntelliJ Terminal, navigate to rails-api:
```bash
cd rails-api
```

3. Create the database:
```bash
bundle exec rails db:create
```

**You should see:**
```
Created database 'shopify_analytics_development'
```

4. Run migrations:
```bash
bundle exec rails db:migrate
```

**You should see:**
```
== 20240115000001 CreateStores: migrating ====
-- create_table(:stores)
== 20240115000001 CreateStores: migrated ====

== 20240115000002 CreateQuestions: migrating ====
-- create_table(:questions)
== 20240115000002 CreateQuestions: migrated ====
```

---

### Step 18: Verify Redis is Running

```bash
redis-cli ping
```

**Should return:** `PONG`

**If not:**
```bash
# Mac:
brew services start redis

# Linux:
sudo systemctl start redis

# Windows: Start redis-server.exe or from Services
```

---

## PART 7: CREATE RUN CONFIGURATIONS (15 minutes)

### Step 19: Create Rails API Run Configuration

1. Click **"Run"** in the top menu
2. Select **"Edit Configurations..."**
3. Click the **"+"** button (top left)
4. Select **"Ruby"** from the dropdown

5. Configure the following fields:

   **Name:** `Rails API Server`
   
   **Ruby SDK:** Select the Ruby SDK you added earlier
   
   **Working directory:** Click the folder icon and select `rails-api` folder
   
   **Ruby script:** `bin/rails`
   
   **Script arguments:** `server -p 3000`
   
   **Environment variables:** 
   - Click the folder icon (📁) on the right
   - Click **"+"** button
   - Click **"Load from file"**
   - Select `rails-api/.env`
   - Click **"OK"**

6. Click **"Apply"**

**Your configuration should look like:**
```
Name: Rails API Server
Ruby SDK: ruby-3.2.0
Working directory: /path/to/shopify-ai-analytics/rails-api
Ruby script: bin/rails
Script arguments: server -p 3000
Environment variables: [Loaded from .env]
```

---

### Step 20: Create Python Agent Run Configuration

1. Still in "Edit Configurations" window
2. Click the **"+"** button again
3. Select **"Python"** from the dropdown

4. Configure the following fields:

   **Name:** `Python Agent`
   
   **Script path:** Click folder icon and select `python-agent/main.py`
   
   **Python interpreter:** Select the venv interpreter you created
   - Should show: `Python 3.11 (python-agent)`
   
   **Working directory:** Click folder icon and select `python-agent` folder
   
   **Environment variables:**
   - Click the folder icon (📁)
   - Click **"+"** button
   - Click **"Load from file"**
   - Select `python-agent/.env`
   - Click **"OK"**

5. Click **"Apply"**

**Your configuration should look like:**
```
Name: Python Agent
Script path: /path/to/shopify-ai-analytics/python-agent/main.py
Python interpreter: Python 3.11 (python-agent)
Working directory: /path/to/shopify-ai-analytics/python-agent
Environment variables: [Loaded from .env]
```

---

### Step 21: Create Compound Configuration (Run Both Together)

1. Still in "Edit Configurations" window
2. Click the **"+"** button
3. Select **"Compound"** from the dropdown

4. Configure:
   **Name:** `Full Stack - Rails + Python`
   
5. Click the **"+"** button in the middle section
6. Select **"Rails API Server"**
7. Click the **"+"** button again
8. Select **"Python Agent"**

9. Click **"Apply"**
10. Click **"OK"**

---

## PART 8: RUN THE APPLICATION (5 minutes)

### Step 22: Start the Services

**Option A: Run Both Together (Recommended)**

1. At the top right of IntelliJ, find the run configuration dropdown
2. Select **"Full Stack - Rails + Python"**
3. Click the green **Play** button ▶️

**You should see:**
- Two tabs open in the Run window at the bottom
- One for Rails API Server
- One for Python Agent

**Option B: Run Individually**

1. Select **"Rails API Server"** from dropdown
2. Click green **Play** button ▶️
3. Wait for Rails to start (look for "Listening on http://0.0.0.0:3000")
4. Select **"Python Agent"** from dropdown
5. Click green **Play** button ▶️

---

### Step 23: Verify Services are Running

**Check Rails API:**

1. Open your web browser
2. Go to: http://localhost:3000/health
3. You should see:
```json
{"status":"healthy"}
```

**Check Python Agent:**

1. In browser, go to: http://localhost:8000
2. You should see:
```json
{
  "service": "Shopify AI Analytics Agent",
  "status": "running",
  "version": "1.0.0"
}
```

**Check Python API Documentation:**

1. Go to: http://localhost:8000/docs
2. You should see FastAPI interactive documentation (Swagger UI)

---

## PART 9: TEST THE API (10 minutes)

### Step 24: Create HTTP Test File

1. In IntelliJ, right-click on project root
2. Select **"New"** → **"File"**
3. Name it: `test-api.http`
4. Click **"OK"**

5. Paste this content:

```http
### Test 1: Health Check - Rails API
GET http://localhost:3000/health

### Test 2: Health Check - Python Agent
GET http://localhost:8000/health

### Test 3: Python Agent Info
GET http://localhost:8000

### Test 4: Ask a Question (will fail without Shopify setup)
POST http://localhost:3000/api/v1/questions
Content-Type: application/json

{
  "store_id": "example-store.myshopify.com",
  "question": "What were my top 5 selling products last week?"
}
```

6. Save the file

---

### Step 25: Run HTTP Tests

1. You'll see green **Play** buttons (▶️) next to each `###` line
2. Click the play button next to **"Test 1: Health Check - Rails API"**
3. A panel will open on the right showing the response
4. You should see: `200 OK` with `{"status":"healthy"}`

5. Click play button next to **"Test 2: Health Check - Python Agent"**
6. Should see: `200 OK` with service info

7. Click play button next to **"Test 3: Python Agent Info"**
8. Should see: `200 OK` with detailed service info

**Test 4 will fail** because we haven't set up Shopify credentials yet. That's expected!

---

## PART 10: OPTIONAL - GET API KEYS (30 minutes)

### Step 26: Get OpenAI API Key (Required for AI features)

1. Go to https://platform.openai.com/signup
2. Create an account (or sign in)
3. Go to https://platform.openai.com/api-keys
4. Click **"Create new secret key"**
5. Name it: "Shopify Analytics Dev"
6. Click **"Create secret key"**
7. **IMPORTANT:** Copy the key immediately (starts with `sk-proj-...`)
8. You won't be able to see it again!

9. Open `python-agent/.env` in IntelliJ
10. Replace:
```env
OPENAI_API_KEY=your_openai_api_key_here
```
With:
```env
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
```
11. Save the file
12. **Restart Python Agent** (click stop ⏹️ then play ▶️)

---

### Step 27: Get Shopify API Credentials (Required for Shopify integration)

1. Go to https://partners.shopify.com/signup
2. Create a Shopify Partner account (it's free!)
3. After signup, go to https://partners.shopify.com
4. Click **"Apps"** in the left sidebar
5. Click **"Create app"**
6. Select **"Create app manually"**
7. Fill in:
   - **App name:** "Shopify AI Analytics Dev"
   - **App URL:** `http://localhost:3000`
   - **Allowed redirection URL(s):** `http://localhost:3000/api/v1/auth/shopify/callback`
8. Click **"Create app"**

9. In the app dashboard:
   - Click **"Configuration"** tab
   - Under "App credentials", you'll see:
     - **API key** (copy this)
     - **API secret key** (click "Show" and copy)

10. Open `rails-api/.env` in IntelliJ
11. Update:
```env
SHOPIFY_API_KEY=your_actual_api_key_here
SHOPIFY_API_SECRET=your_actual_secret_here
```
12. Save the file
13. **Restart Rails API** (click stop ⏹️ then play ▶️)

---

## PART 11: DEBUGGING & TROUBLESHOOTING

### Step 28: Set Up Debugging

**To Debug Rails:**
1. Open any Ruby file (e.g., `rails-api/app/controllers/api/v1/questions_controller.rb`)
2. Click in the left margin (gutter) next to a line number
3. A red dot appears (breakpoint)
4. Select **"Rails API Server"** configuration
5. Click the **Debug** button 🐛 (next to Play button)
6. When code hits the breakpoint, execution pauses
7. Use the debug panel to inspect variables

**To Debug Python:**
1. Open any Python file (e.g., `python-agent/app/agents/shopify_agent.py`)
2. Click in the left margin to set breakpoint
3. Select **"Python Agent"** configuration
4. Click the **Debug** button 🐛
5. When code hits breakpoint, inspect variables in debug panel

---

### Common Issues and Solutions

**Issue 1: "Port 3000 already in use"**
```bash
# Find what's using the port
lsof -i :3000  # Mac/Linux
netstat -ano | findstr :3000  # Windows

# Kill the process
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows
```

**Issue 2: "Bundle install fails"**
```bash
# Update RubyGems and Bundler
gem update --system
gem install bundler

# Try again
cd rails-api
bundle install
```

**Issue 3: "Python packages not installing"**
```bash
# Make sure venv is activated
cd python-agent
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip

# Try again
pip install -r requirements.txt
```

**Issue 4: "Database connection refused"**
```bash
# Check if PostgreSQL is running
psql --version

# Start PostgreSQL
brew services start postgresql@14  # Mac
sudo systemctl start postgresql    # Linux
# Windows: Start from Services app
```

**Issue 5: "Redis connection refused"**
```bash
# Check if Redis is running
redis-cli ping

# Start Redis
brew services start redis          # Mac
sudo systemctl start redis         # Linux
# Windows: Start redis-server.exe
```

**Issue 6: "Rails secret key error"**
```bash
cd rails-api
bundle exec rails secret
# Copy output and paste in rails-api/.env as SECRET_KEY_BASE
```

---

## PART 12: VIEWING LOGS

### Step 29: View Application Logs

**In IntelliJ Run Window:**
1. Click `View` → `Tool Windows` → `Run` (or press `Alt+4`)
2. You'll see tabs for each running service
3. Click on a tab to see its logs
4. Use the search box (🔍) to filter logs
5. Use the scroll lock button to auto-scroll

**Rails Log File:**
- Location: `rails-api/log/development.log`
- Double-click to open in IntelliJ
- Auto-refreshes as new logs are written

**Python Logs:**
- Appear in the Run window console
- Can configure file logging if needed

---

## PART 13: STOPPING THE APPLICATION

### Step 30: Stop Services

**Option A: Stop Button**
1. In the Run window, click the red **Stop** button ⏹️
2. If running compound configuration, stops all services

**Option B: Keyboard Shortcut**
- Press `Ctrl+F2` (Windows/Linux)
- Press `Cmd+F2` (Mac)
- Select which service to stop

**Option C: Stop All**
1. Click the dropdown next to stop button
2. Select **"Stop All"**

---

## 🎉 CONGRATULATIONS!

You've successfully set up and run the Shopify AI Analytics application in IntelliJ IDEA!

## Next Steps:

1. ✅ **Test the API** using the HTTP test file
2. ✅ **Get API keys** (OpenAI and Shopify)
3. ✅ **Create a test Shopify store** (free development store)
4. ✅ **Connect your store** via OAuth
5. ✅ **Ask questions** and see AI-powered analytics!

## Quick Reference:

**Start Application:**
- Select "Full Stack - Rails + Python"
- Click ▶️

**Stop Application:**
- Click ⏹️

**View Logs:**
- `Alt+4` (Windows/Linux) or `Cmd+4` (Mac)

**Debug:**
- Set breakpoints (click left margin)
- Click 🐛 instead of ▶️

**Test API:**
- Open `test-api.http`
- Click ▶️ next to requests

## Need Help?

- Check `docs/architecture.md` for system design
- Check `docs/agent-flow.md` for AI agent details
- Check `docs/api-examples.md` for API examples
- Check IntelliJ logs for error messages

Happy coding! 🚀