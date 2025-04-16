# Tablog MCP Server

This server allows your LLM to search for restaurants in [Tablog](https://tabelog.com/en/rstLst/), a website that is used locally in Japan to rate restaurants and often works better than Google Maps for planning which restaurants to visit in Japan!

Right now the server is only able to search for restaurants given a cuisine and a location in Tokyo, and can filter by max cost in Yen. There are a lot more filters that can be added!

## Running Locally

To run this server locally for development or testing:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/sgoel97/tablog-mcp
    cd tablog-mcp
    ```

2.  **Install uv, then sync dependencies using uv:**

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh # download uv if not already installed
    uv sync
    ```

3.  **Run the server in development mode:**
    ```bash
    uv run mcp dev python src/server.py
    ```

The server will start alongside the MCP Inspector, which can then be used for testing.

## Adding to Claude Desktop

To add this server to your config, add the following to your Claude config in `claude_desktop_config.json`.

```json
"Tablog Restaurant Guide": {
    "command": "/opt/homebrew/anaconda3/bin/uv",
    "args": [
    "run",
    "--with",
    "mcp[cli]",
    "--with",
    "requests",
    "--with",
    "beautifulsoup4",
    "mcp",
    "run",
    "/Users/samarthgoel/Desktop/tablog-mcp/src/server.py"
    ]
}
```

## Future Improvements

- [ ] Add filtering by date/time and number of people
- [ ] Make search more generic, not requiring specific area and cuisine codes
- [ ] Return a smarter segment of text in the restaurant's `text` field
- [ ] Allow search over more restaurants at once
