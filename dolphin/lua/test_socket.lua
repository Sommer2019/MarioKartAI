-- test_socket.lua
-- Simple test to verify the socket module works in Dolphin Lua environment

-- Test that socket module can be required
local socket = require("socket")
print("Socket module loaded successfully!")

-- Test UDP socket creation
local udp_send = socket.udp()
print("UDP send socket created")

local udp_recv = socket.udp()
print("UDP receive socket created")

-- Test socket configuration
udp_send:settimeout(0)
udp_recv:settimeout(0)
udp_recv:setsockname("*", 12346)
print("Socket configuration completed")

-- Test sending data
local test_data = "1.0,2.0,3.0,0.5,4.2,1"
local result = udp_send:sendto(test_data, "127.0.0.1", 12345)
if result then
    print("Data sent successfully: " .. test_data)
else
    print("Failed to send data")
end

-- Test receiving data (will be nil since no data is available in test)
local received = udp_recv:receive()
if received then
    print("Received data: " .. received)
else
    print("No data received (expected in test)")
end

print("Socket test completed successfully!")