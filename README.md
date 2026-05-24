# BugPulse - Production-Ready Bug Tracking API

A production-ready FastAPI application for bug tracking, notification management, and real-time dashboards.

## Features

✅ **External API Integration** - Fetch bugs from external APIs with authentication
✅ **SQLite Database** - Persistent storage with SQLAlchemy ORM
✅ **Google Chat Integration** - Send formatted notifications to Google Chat
✅ **Duplicate Prevention** - Automatically avoid duplicate notifications
✅ **Background Scheduler** - APScheduler runs sync job every 5 minutes
✅ **REST API** - Full CRUD operations for bug management
✅ **HTML Dashboard** - Beautiful real-time dashboard with statistics
✅ **Error Handling** - Comprehensive error handling and logging
✅ **Production Ready** - Proper project structure and best practices

## Project Structure

```
BugPulse/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Configuration management
│   ├── database.py              # Database models and setup
│   ├── schemas.py               # Pydantic schemas
│   ├── services.py              # Business logic services
│   ├── routes.py                # REST API routes
│   ├── dashboard.py             # HTML dashboard
│   └── scheduler.py             # Background scheduler
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── Dockerfile                   # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── .gitignore                  # Git ignore rules
├── README.md                    # Project documentation
└── run.py                       # Application entry point
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/SKA-MALIK/BugPulse.git
cd BugPulse
```

### 2. Create virtual environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
# External API Configuration
EXTERNAL_API_URL=https://your-api.com/bugs
EXTERNAL_API_KEY=your_secret_api_key

# Google Chat Webhook
GOOGLE_CHAT_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/YOUR_SPACE/messages?key=YOUR_KEY

# Other settings
SCHEDULER_INTERVAL=5
DEBUG=False
LOG_LEVEL=INFO
```

## Running the Application

### Development Mode
```bash
python -m uvicorn app.main:app --reload --port 8000
```

### Production Mode
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use the run script:
```bash
python run.py
```

The application will start at `http://localhost:8000`

## API Endpoints

### Bugs Management
- `GET /api/v1/bugs/` - List all bugs with pagination and filtering
- `GET /api/v1/bugs/{bug_id}` - Get a specific bug
- `POST /api/v1/bugs/` - Create a new bug
- `PUT /api/v1/bugs/{bug_id}` - Update a bug
- `DELETE /api/v1/bugs/{bug_id}` - Delete a bug
- `GET /api/v1/bugs/stats/summary` - Get bug statistics

### Dashboard
- `GET /dashboard` - HTML dashboard with real-time statistics

### Health
- `GET /health` - Health check endpoint
- `GET /` - Root endpoint with API information

## API Usage Examples

### List Bugs with Filtering
```bash
curl "http://localhost:8000/api/v1/bugs/?skip=0&limit=10&status=open&severity=critical"
```

### Get Bug Details
```bash
curl "http://localhost:8000/api/v1/bugs/1"
```

### Create a Bug
```bash
curl -X POST "http://localhost:8000/api/v1/bugs/" \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "BUG-001",
    "title": "Login button not working",
    "description": "Users cannot click the login button",
    "severity": "critical"
  }'
```

### Update a Bug
```bash
curl -X PUT "http://localhost:8000/api/v1/bugs/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "closed",
    "severity": "high"
  }'
```

### Get Statistics
```bash
curl "http://localhost:8000/api/v1/bugs/stats/summary"
```

## Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Background Scheduler

The application runs a background scheduler that:
1. **Syncs bugs every 5 minutes** from the external API
2. **Detects new bugs** automatically
3. **Sends notifications** to Google Chat for new bugs
4. **Marks bugs as notified** to prevent duplicates
5. **Handles errors gracefully** with logging

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| EXTERNAL_API_URL | - | External API endpoint for fetching bugs |
| EXTERNAL_API_KEY | - | API key for authentication |
| GOOGLE_CHAT_WEBHOOK_URL | - | Google Chat webhook for notifications |
| DATABASE_URL | sqlite:///./bugs.db | SQLite database URL |
| SCHEDULER_INTERVAL | 5 | Scheduler interval in minutes |
| API_TITLE | BugPulse API | API title |
| API_VERSION | 1.0.0 | API version |
| DEBUG | False | Debug mode |
| LOG_LEVEL | INFO | Logging level |

## Error Handling

The application includes comprehensive error handling:
- ✅ Connection timeouts
- ✅ HTTP errors
- ✅ Database errors
- ✅ Invalid input validation
- ✅ Duplicate prevention
- ✅ Detailed logging

All errors are logged with context and appropriate HTTP status codes are returned.

## Logging

Logs are configured based on the `LOG_LEVEL` environment variable:
- **DEBUG**: Detailed information for debugging
- **INFO**: General information about application operations
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures

Log format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

## Docker Deployment

### Build Docker Image
```bash
docker build -t bugpulse:latest .
```

### Run with Docker
```bash
docker run -p 8000:8000 \
  -e EXTERNAL_API_URL=https://your-api.com/bugs \
  -e EXTERNAL_API_KEY=your_key \
  -e GOOGLE_CHAT_WEBHOOK_URL=your_webhook \
  bugpulse:latest
```

### Docker Compose
```bash
docker-compose up -d
```

## Database Schema

### Bugs Table
```sql
CREATE TABLE bugs (
    id INTEGER PRIMARY KEY,
    external_id VARCHAR UNIQUE NOT NULL,
    title VARCHAR NOT NULL,
    description VARCHAR,
    severity VARCHAR,
    status VARCHAR DEFAULT 'open',
    notified BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Best Practices Implemented

1. **Separation of Concerns** - Clear division between routes, services, and database layers
2. **Configuration Management** - Environment-based configuration
3. **Error Handling** - Comprehensive try-catch blocks and error logging
4. **Logging** - Detailed logging at all levels
5. **Database Management** - Proper session handling and transaction management
6. **API Design** - RESTful endpoints with proper HTTP status codes
7. **Input Validation** - Pydantic schemas for request/response validation
8. **Documentation** - Inline code comments and API documentation
9. **Security** - CORS middleware and secure headers
10. **Scalability** - Asynchronous operations and efficient queries

## Troubleshooting

### Database Lock Error
If you get a database lock error, ensure only one instance is running and consider using PostgreSQL for production.

### Scheduler Not Running
Check the logs for errors. Ensure APScheduler is properly installed: `pip install APScheduler`

### No Notifications Sent
1. Verify the Google Chat webhook URL is correct
2. Check the logs for HTTP errors
3. Ensure the external API is returning data

### Port Already in Use
Change the port in the command: `uvicorn app.main:app --port 8001`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.

## Changelog

### v1.0.0 (Initial Release)
- ✅ FastAPI application setup
- ✅ SQLite database integration
- ✅ External API client
- ✅ Google Chat notifications
- ✅ Background scheduler
- ✅ REST API endpoints
- ✅ HTML dashboard
- ✅ Comprehensive logging and error handling
