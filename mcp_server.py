#!/usr/bin/env python3

import asyncio
import logging
from typing import Any, Sequence
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
from pydantic import AnyUrl
import json
from scraper import HackerNewsScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hn-job-scraper")

# Initialize the MCP server
app = Server("hn-job-scraper")

# Initialize scraper
scraper = HackerNewsScraper()

@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources (cached job data)"""
    return [
        Resource(
            uri=AnyUrl("hn://jobs/latest"),
            name="Latest HackerNews Jobs",
            description="Most recent job postings from HackerNews Who's Hiring thread",
            mimeType="application/json",
        ),
        Resource(
            uri=AnyUrl("hn://jobs/search"),
            name="Search Jobs",
            description="Search through job postings",
            mimeType="application/json",
        ),
    ]

@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """Read a specific resource"""
    if uri.scheme != "hn":
        raise ValueError(f"Unsupported URI scheme: {uri.scheme}")
    
    path = str(uri).replace("hn://", "")
    
    if path == "jobs/latest":
        # Get latest job postings
        jobs = scraper.scrape_job_postings()
        return json.dumps(jobs, indent=2)
    
    elif path == "jobs/search":
        # Return search instructions
        return json.dumps({
            "message": "Use the search_jobs tool to search through job postings",
            "example": "search_jobs with query 'python' or 'remote' or 'senior'"
        }, indent=2)
    
    else:
        raise ValueError(f"Unknown resource path: {path}")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="search_jobs",
            description="Search through HackerNews job postings",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'python', 'remote', 'senior developer')"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_job_details",
            description="Get detailed information about a specific job posting",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "The job posting ID"
                    }
                },
                "required": ["job_id"]
            }
        ),
        Tool(
            name="refresh_jobs",
            description="Refresh job postings from HackerNews (clears cache)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "search_jobs":
        query = arguments.get("query", "")
        if not query:
            return [TextContent(type="text", text="Please provide a search query")]
        
        # Get job postings and search
        jobs = scraper.scrape_job_postings()
        matching_jobs = scraper.search_jobs(query, jobs)
        
        if not matching_jobs:
            return [TextContent(
                type="text", 
                text=f"No jobs found matching '{query}'"
            )]
        
        # Format results
        results = []
        for job in matching_jobs[:20]:  # Limit to first 20 results
            job_summary = {
                "id": job["id"],
                "author": job["author"],
                "timestamp": job["timestamp"],
                "preview": job["text"][:300] + "..." if len(job["text"]) > 300 else job["text"]
            }
            results.append(job_summary)
        
        return [TextContent(
            type="text",
            text=f"Found {len(matching_jobs)} jobs matching '{query}'. Showing first {len(results)}:\n\n" +
                 json.dumps(results, indent=2)
        )]
    
    elif name == "get_job_details":
        job_id = arguments.get("job_id", "")
        if not job_id:
            return [TextContent(type="text", text="Please provide a job ID")]
        
        # Get job postings and find the specific job
        jobs = scraper.scrape_job_postings()
        job = next((j for j in jobs if j["id"] == job_id), None)
        
        if not job:
            return [TextContent(
                type="text",
                text=f"Job with ID '{job_id}' not found"
            )]
        
        return [TextContent(
            type="text",
            text=json.dumps(job, indent=2)
        )]
    
    elif name == "refresh_jobs":
        # Clear cache by removing cache files
        import os
        import glob
        cache_files = glob.glob(os.path.join(scraper.cache_dir, "*.json"))
        for cache_file in cache_files:
            os.remove(cache_file)
        
        # Fetch fresh data
        jobs = scraper.scrape_job_postings()
        
        return [TextContent(
            type="text",
            text=f"Refreshed job postings. Found {len(jobs)} jobs."
        )]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="hn-job-scraper",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())