# HackerNews Job Scraper

A Python-based job scraper that extracts job postings from HackerNews "Who's Hiring" threads and exposes them via an MCP (Model Context Protocol) server for Claude Desktop integration.

## Features

- **HackerNews Scraper**: Extracts job postings from HN threads and converts them to structured JSON
- **MCP Server**: Exposes scraped data through Model Context Protocol for Claude Desktop
- **Caching**: File-based caching system to avoid repeated requests
- **Search**: Search through job postings by keywords
- **Job Details**: Get full details of specific job postings

## Quick Start

### 1. Setup Environment

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Test the Scraper

```bash
# Run the scraper directly
python scraper.py
```

This will scrape the default HackerNews thread and show how many job postings were found.

### 3. Configure Claude Desktop

Add the following to your Claude Desktop settings (usually at `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "hn-job-scraper": {
      "command": "python3",
      "args": ["/path/to/your/project/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/your/project"
      }
    }
  }
}
```

**Important**: Replace `/path/to/your/project` with the actual path to this project directory.

### 4. Start Using with Claude Desktop

Once configured, you can use these tools in Claude Desktop:

- **Search Jobs**: `search_jobs` - Search job postings by keywords (e.g., "python", "remote", "senior")
- **Get Job Details**: `get_job_details` - Get full details of a specific job posting
- **Refresh Jobs**: `refresh_jobs` - Clear cache and fetch fresh job data

## Usage Examples

### Command Line Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run scraper
python scraper.py

# Start MCP server (usually called by Claude Desktop)
python mcp_server.py
```

### Claude Desktop Integration

Once configured, you can ask Claude Desktop:

- "Search for Python jobs in the latest HackerNews hiring thread"
- "Find remote work opportunities"
- "Show me senior developer positions"
- "Get details for job posting ID 12345"

## Project Structure

```
hackernews-jobscraper/
├── scraper.py              # Core scraping functionality
├── mcp_server.py           # MCP server implementation
├── requirements.txt        # Python dependencies
├── claude_desktop_config.json  # Example Claude Desktop config
├── cache/                  # Cached job data (created automatically)
└── README.md              # This file
```

## How It Works

1. **Scraping**: The scraper fetches job postings from HackerNews "Who's Hiring" threads
2. **Caching**: Results are cached locally to avoid repeated requests (1-hour cache)
3. **MCP Server**: Exposes the data through Model Context Protocol
4. **Claude Integration**: Claude Desktop can search and analyze job postings

## Configuration

### Default HackerNews Thread

The scraper defaults to thread ID `44434574`. You can change this by modifying the `scrape_job_postings()` call in `scraper.py`.

### Cache Settings

Cache files are stored in the `cache/` directory and expire after 1 hour. This can be modified in the `HackerNewsScraper` class.

## Troubleshooting

### Claude Desktop Not Finding Server

1. Ensure the paths in `claude_desktop_config.json` are absolute paths
2. Make sure the virtual environment is activated
3. Check that all dependencies are installed
4. Restart Claude Desktop after configuration changes

### No Job Postings Found

1. Check your internet connection
2. Verify the HackerNews thread ID is valid
3. Try refreshing the job data using the `refresh_jobs` tool

## Development

### Running Tests

```bash
# Test scraper functionality
python scraper.py

# Test MCP server (requires Claude Desktop or MCP client)
python mcp_server.py
```

### Adding New Features

The project is designed to be extensible. You can:

- Add new scraping sources
- Implement additional search filters
- Enhance job posting metadata
- Add data export functionality
# hn_candidate_mcp
