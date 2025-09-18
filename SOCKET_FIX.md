# Socket Module Fix for Dolphin Lua

## Problem
The original Mario Kart AI project uses LuaSocket for UDP communication between the Dolphin emulator's Lua script and the Python AI agent. However, Dolphin's Lua environment doesn't include the LuaSocket library by default, causing the error:

```
Lua Error: module 'socket' not found
```

## Solution
This repository now includes a file-based communication system that replaces UDP sockets with simple file I/O operations. This approach is compatible with Dolphin's standard Lua environment without requiring additional dependencies.

## How It Works

### File-Based Communication
- **Lua to Python**: Lua writes state data to `lua_to_python.txt`
- **Python to Lua**: Python writes action data to `python_to_lua.txt`
- Both files are continuously monitored and cleared after reading to prevent data conflicts

### Modified Files
1. **`dolphin/lua/socket.lua`** - Custom socket module that emulates LuaSocket API using file I/O
2. **`python/mk_pro_ai_loop.py`** - Updated to use file-based communication instead of UDP sockets

## Usage
The usage remains the same as documented in `START_GUIDE.md`:

1. Start Dolphin and load Mario Kart Wii
2. Load the Lua script `dolphin/lua/mkw_pro_ai.lua` in Dolphin's Lua Scripting window
3. Run the Python agent: `python mk_pro_ai_loop.py`

## Compatibility
- ✅ Works with standard Dolphin installations
- ✅ No additional dependencies required
- ✅ Maintains the same API as the original LuaSocket implementation
- ✅ Cross-platform compatibility (Windows, macOS, Linux)

## Performance
While file-based communication is slightly slower than UDP sockets, the performance difference is negligible for Mario Kart AI applications since the communication frequency is tied to the game's frame rate (typically 60 FPS).