# Running Shopify AI Analytics in IntelliJ IDEA

This guide will help you set up and run the project in IntelliJ IDEA.

## Prerequisites

1. **IntelliJ IDEA Ultimate** (Community Edition has limited Ruby support)
2. **Ruby 3.2+** installed on your system
3. **Python 3.11+** installed on your system
4. **PostgreSQL 14+** installed and running
5. **Redis** installed and running

## Step-by-Step Setup

### 1. Install Required Plugins

Open IntelliJ IDEA and install these plugins:
- **Ruby** (for Rails support)
- **Python** (for Python/FastAPI support)
- **Database Tools and SQL** (usually pre-installed)
- **Docker** (optional, for Docker Compose)

**How to install:**
1. Go to `File` → `Settings` (Windows/Linux) or `IntelliJ IDEA` → `Preferences` (Mac)
2. Navigate to `Plugins`
3. Search for each plugin and click `Install`
4. Restart IntelliJ IDEA

### 2. Clone and Open Project

```bash
# Clone the repository
git clone https://github.com/Amansingh80/shopify-ai-analytics.git
cd shopify-ai-analytics
```

**In IntelliJ IDEA:**
1. `File` → `Open`
2. Select the `shopify-ai-analytics` folder
3. Click `OK`

### 3. Configure Ruby SDK

1. Go to `File` → `Project Structure` → `SDKs`
2. Click `+` → `Add Ruby SDK`
3. Select your Ruby installation (e.g., `/usr/local/bin/ruby` or `C:\Ruby32\bin\ruby.exe`)
4. Click `OK`

**For Rails API:**
1. Right-click on `rails-api` folder
2. Select `Mark Directory as` → `Sources Root`

### 4. Configure Python Interpreter

1. Go to `File` → `Project Structure` → `SDKs`
2. Click `+` → `Add Python SDK`
3. Choose `Virtualenv Environment` → `New`
4. Set location: `python-agent/venv`
5. Base interpreter: Select your Python 3.11+ installation
6. Click `OK`

**For Python Agent:**
1. Right-click on `python-agent` folder
2. Select `Mark Directory as` → `Sources Root`

### 5. Set Up Environment Variables

#### Rails API Environment

1. Copy the example file:
   ```bash
   cp rails-api/.env.example rails-api/.env
   ```

2. Edit `rails-api/.env`:
   ```env
   SHOPIFY_API_KEY=your_shopify_api_key_here
   SHOPIFY_API_SECRET=your_shopify_api_secret_here
   PYTHON_AGENT_URL=http://localhost:8000
   DATABASE_URL=postgresql://postgres:postgres@localhost/shopify_analytics_development
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY_BASE=generate_with_rails_secret
   RAILS_ENV=development
   RAILS_LOG_LEVEL=debug
   ```

3. Generate Rails secret:
   ```bash
   cd rails-api
   bundle exec rails secret
   # Copy the output and paste it as SECRET_KEY_BASE
   ```

#### Python Agent Environment

1. Copy the example file:
   ```bash
   cp python-agent/.env.example python-agent/.env
   ```

2. Edit `python-agent/.env`:
   ```env
   OPENAI_API_KEY=sk-proj-your_openai_key_here
   SHOPIFY_API_VERSION=2024-01
   REDIS_URL=redis://localhost:6379/1
   LOG_LEVEL=INFO
   ```

### 6. Install Dependencies

#### Rails API Dependencies

**Option A: Using IntelliJ Terminal**
1. Open Terminal in IntelliJ (`View` → `Tool Windows` → `Terminal`)
2. Navigate to rails-api:
   ```bash
   cd rails-api
   bundle install
   ```

**Option B: Using Run Configuration**
1. Right-click on `rails-api/Gemfile`
2. Select `Run 'bundle install'`

#### Python Agent Dependencies

**In IntelliJ Terminal:**
```bash
cd python-agent
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 7. Set Up Database

**In IntelliJ Terminal:**
```bash
cd rails-api

# Create database
bundle exec rails db:create

# Run migrations
bundle exec rails db:migrate

# (Optional) Seed data
bundle exec rails db:seed
```

### 8. Start PostgreSQL and Redis

**Option A: Using System Services**
```bash
# PostgreSQL
# Mac (Homebrew):
brew services start postgresql

# Linux:
sudo systemctl start postgresql

# Windows: Start from Services app

# Redis
# Mac (Homebrew):
brew services start redis

# Linux:
sudo systemctl start redis

# Windows: Start redis-server.exe
```

**Option B: Using Docker (Recommended)**
```bash
# In project root
docker-compose up postgres redis -d
```

### 9. Create Run Configurations

#### Configuration 1: Rails API Server

1. Click `Run` → `Edit Configurations`
2. Click `+` → `Ruby`
3. Configure:
   - **Name:** `Rails API Server`
   - **Ruby SDK:** Select your Ruby SDK
   - **Working directory:** `[project-root]/rails-api`
   - **Ruby script:** `bin/rails`
   - **Script arguments:** `server -p 3000`
   - **Environment variables:** Click folder icon and load from `.env` file
4. Click `Apply` and `OK`

#### Configuration 2: Python Agent

1. Click `Run` → `Edit Configurations`
2. Click `+` → `Python`
3. Configure:
   - **Name:** `Python Agent`
   - **Script path:** Select `python-agent/main.py`
   - **Python interpreter:** Select the venv interpreter you created
   - **Working directory:** `[project-root]/python-agent`
   - **Environment variables:** Click folder icon and load from `.env` file
   - **Parameters:** (leave empty, uvicorn config is in main.py)
4. Click `Apply` and `OK`

**Alternative for Python (using uvicorn directly):**
1. Click `+` → `Python`
2. Configure:
   - **Name:** `Python Agent (uvicorn)`
   - **Module name:** `uvicorn` (instead of Script path)
   - **Parameters:** `main:app --reload --host 0.0.0.0 --port 8000`
   - **Python interpreter:** Select the venv interpreter
   - **Working directory:** `[project-root]/python-agent`
   - **Environment variables:** Load from `.env`

#### Configuration 3: Compound (Run Both Together)

1. Click `Run` → `Edit Configurations`
2. Click `+` → `Compound`
3. Configure:
   - **Name:** `Full Stack`
   - Click `+` and add `Rails API Server`
   - Click `+` and add `Python Agent`
4. Click `Apply` and `OK`

### 10. Run the Application

**Option A: Run Individually**
1. Select `Rails API Server` from the run configuration dropdown
2. Click the green play button ▶️
3. Wait for Rails to start (watch console output)
4. Select `Python Agent` from the dropdown
5. Click the green play button ▶️

**Option B: Run Together**
1. Select `Full Stack` from the run configuration dropdown
2. Click the green play button ▶️
3. Both services will start simultaneously

### 11. Verify Everything is Running

**Check Rails API:**
- Open browser: http://localhost:3000/health
- Should see: `{"status":"healthy"}`

**Check Python Agent:**
- Open browser: http://localhost:8000
- Should see: `{"service":"Shopify AI Analytics Agent","status":"running"}`

**Check Python Agent Docs:**
- Open browser: http://localhost:8000/docs
- Should see FastAPI interactive documentation

### 12. Database Tool Window (Optional)

1. Open `View` → `Tool Windows` → `Database`
2. Click `+` → `Data Source` → `PostgreSQL`
3. Configure:
   - **Host:** localhost
   - **Port:** 5432
   - **Database:** shopify_analytics_development
   - **User:** postgres
   - **Password:** postgres
4. Click `Test Connection`
5. Click `OK`

Now you can browse tables, run queries, etc.

### 13. Testing the API

**Using IntelliJ HTTP Client:**

1. Create a file: `test-requests.http` in project root
2. Add this content:

```http
### Health Check - Rails
GET http://localhost:3000/health

### Health Check - Python
GET http://localhost:8000/health

### Ask a Question
POST http://localhost:3000/api/v1/questions
Content-Type: application/json

{
  "store_id": "example-store.myshopify.com",
  "question": "What were my top 5 selling products last week?"
}

### Get Question by ID
GET http://localhost:3000/api/v1/questions/1

### List Questions
GET http://localhost:3000/api/v1/questions?store_id=example-store.myshopify.com&page=1
```

3. Click the green play button next to each request to execute

### 14. Debugging

**Debug Rails API:**
1. Set breakpoints in Ruby code (click left margin)
2. Select `Rails API Server` configuration
3. Click the debug button 🐛 instead of run

**Debug Python Agent:**
1. Set breakpoints in Python code (click left margin)
2. Select `Python Agent` configuration
3. Click the debug button 🐛 instead of run

### 15. Common Issues and Solutions

#### Issue: "Bundle install fails"
**Solution:**
```bash
# Update bundler
gem install bundler
gem update --system
```

#### Issue: "Python packages not found"
**Solution:**
```bash
# Make sure venv is activated
cd python-agent
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall
pip install --upgrade pip
pip install -r requirements.txt
```

#### Issue: "Database connection failed"
**Solution:**
```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT version();"

# If not running, start it
brew services start postgresql  # Mac
sudo systemctl start postgresql # Linux
```

#### Issue: "Redis connection failed"
**Solution:**
```bash
# Check Redis is running
redis-cli ping

# Should return: PONG

# If not running, start it
brew services start redis       # Mac
sudo systemctl start redis      # Linux
```

#### Issue: "Port already in use"
**Solution:**
```bash
# Find process using port 3000
lsof -i :3000  # Mac/Linux
netstat -ano | findstr :3000  # Windows

# Kill the process
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows
```

### 16. Hot Reload

Both services support hot reload:
- **Rails:** Automatically reloads on code changes
- **Python:** Using `--reload` flag in uvicorn

Just save your files and changes will be reflected automatically!

### 17. Viewing Logs

**In IntelliJ:**
- Logs appear in the `Run` tool window at the bottom
- Each service has its own tab
- Use the search/filter features to find specific log entries

**Log Files:**
- Rails: `rails-api/log/development.log`
- Python: Console output (can configure file logging)

### 18. Stopping the Application

**Option A: Stop Button**
- Click the red stop button ⏹️ in the Run tool window

**Option B: Keyboard Shortcut**
- `Ctrl+F2` (Windows/Linux)
- `Cmd+F2` (Mac)

## Quick Start Checklist

- [ ] Install IntelliJ IDEA Ultimate
- [ ] Install Ruby, Python, PostgreSQL, Redis
- [ ] Install IntelliJ plugins (Ruby, Python)
- [ ] Clone repository
- [ ] Configure Ruby SDK
- [ ] Configure Python interpreter
- [ ] Copy and edit `.env` files
- [ ] Install Rails dependencies (`bundle install`)
- [ ] Install Python dependencies (`pip install -r requirements.txt`)
- [ ] Create database (`rails db:create db:migrate`)
- [ ] Start PostgreSQL and Redis
- [ ] Create run configurations
- [ ] Run the application
- [ ] Test with HTTP requests

## Next Steps

Once everything is running:
1. Set up Shopify Partner account
2. Create a Shopify app
3. Configure OAuth credentials
4. Test with real Shopify store
5. Start developing features!

## Need Help?

- Check the main README.md for architecture details
- Review docs/architecture.md for system design
- See docs/api-examples.md for API usage
- Check IntelliJ logs for error messages

Happy coding! 🚀