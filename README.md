# Tablog MCP Server

This server allows your LLM to search for restaurants in [Tablog](https://tabelog.com/en/rstLst/), a website that is used locally in Japan to rate restaurants and often works better than Google Maps for planning which restaurants to visit in Japan!

Right now the server is only able to search for restaurants given a cuisine and a location in Tokyo, and can filter by max cost in Yen. There are a lot more filters that can be added!

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

---

[ ] Add filtering by date/time and number of people
[ ] Make search more generic, not requiring specific area and cuisine codes
[ ] Return a smarter segment of text in the restaurant's `text` field
[ ] Allow search over more restaurants at once
