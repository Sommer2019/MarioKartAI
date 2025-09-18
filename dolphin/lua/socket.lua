-- socket.lua: Simple file-based socket emulation for Dolphin Lua
-- This module provides basic UDP-like functionality using file I/O
-- since Dolphin doesn't include LuaSocket

local socket = {}

-- File paths for communication
local SEND_FILE = "lua_to_python.txt"
local RECV_FILE = "python_to_lua.txt"

-- UDP socket emulation
local udp_socket = {}
udp_socket.__index = udp_socket

function udp_socket:settimeout(timeout)
    self.timeout = timeout
end

function udp_socket:setsockname(host, port)
    self.host = host
    self.port = port
    -- Clear receive file on initialization
    local file = io.open(RECV_FILE, "w")
    if file then
        file:close()
    end
end

function udp_socket:sendto(data, host, port)
    local file = io.open(SEND_FILE, "w")
    if file then
        file:write(data)
        file:close()
        return #data
    end
    return nil, "file write error"
end

function udp_socket:receive()
    local file = io.open(RECV_FILE, "r")
    if file then
        local data = file:read("*all")
        file:close()
        if data and data ~= "" then
            -- Clear the file after reading
            local clear_file = io.open(RECV_FILE, "w")
            if clear_file then
                clear_file:close()
            end
            return data:gsub("\n", ""):gsub("\r", "") -- Remove newlines
        end
    end
    return nil
end

function socket.udp()
    local sock = {}
    setmetatable(sock, udp_socket)
    sock.timeout = 0
    sock.host = nil
    sock.port = nil
    return sock
end

return socket