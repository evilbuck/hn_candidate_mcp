# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**HackerNews Job Scraper** is a resume filtering and candidate analysis tool that:
- Scrapes job postings from HackerNews "Who's Hiring" threads
- Uses Claude AI (Anthropic API) to parse and filter candidates based on job descriptions
- Converts scraped data into structured format with metadata
- Exposes an MCP (Model Context Protocol) server for Claude Desktop integration
- Implements caching for scraped data

## Current Project Status

This is a **newly initialized project** with only the conceptual framework defined. The actual implementation has not yet begun.

### Existing Files
- `README.md` - Project description and requirements
- `.claude/settings.local.json` - Claude Code configuration

## Expected Technology Stack

Based on the project requirements, the implementation will likely involve:
- **Python** - Primary language for scraping, AI integration, and MCP server
- **Claude AI API** - For resume analysis and filtering
- **Web scraping libraries** - BeautifulSoup, requests, or similar
- **MCP Protocol** - For Claude Desktop integration
- **Caching system** - Redis, SQLite, or file-based caching
- **Data processing** - JSON handling, possibly pandas

## Development Setup Commands

*Note: These commands are anticipated for when the project is implemented*

### Python Environment Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies (when requirements.txt exists)
pip install -r requirements.txt
```

### Expected Development Commands
```bash
# Run the scraper
python main.py

# Start MCP server
python mcp_server.py

# Run tests (when implemented)
python -m pytest

# Lint code (when implemented)
flake8 .
black .
```

## Project Architecture (Planned)

The project is expected to have these core components:

### 1. HackerNews Scraper
- Scrapes job postings from specified HN threads
- Parses HTML and extracts relevant job posting data
- Converts to structured format (JSON)

### 2. Claude AI Integration
- Uses Anthropic API for candidate analysis
- Processes job descriptions and requirements
- Filters and ranks candidates based on criteria

### 3. MCP Server
- Exposes Model Context Protocol server
- Integrates with Claude Desktop
- Provides structured access to scraped and processed data

### 4. Caching Layer
- Stores scraped data to avoid repeated requests
- Implements cache invalidation strategies
- Optimizes API usage and performance

### 5. Data Processing
- Metadata extraction from job postings
- Candidate profile analysis
- Structured data output

## Development Notes

- The project is in initialization phase - no implementation code exists yet
- Use `python3` command (not `python`) based on system environment
- Project will likely need environment variables for API keys
- Consider implementing proper error handling for web scraping
- MCP server implementation will need to follow MCP protocol specifications

## Next Implementation Steps

1. Initialize Git repository
2. Create Python virtual environment and requirements.txt
3. Implement basic HackerNews scraper
4. Set up Claude AI API integration
5. Build MCP server framework
6. Add caching mechanism
7. Create proper project structure and documentation