local socket = require("socket")
local host = "127.0.0.1"
local port_send = 12345
local port_recv = 12346

local udp_send = socket.udp()
udp_send:settimeout(0)
local udp_recv = socket.udp()
udp_recv:settimeout(0)
udp_recv:setsockname("*", port_recv)

local function readKartData()
    local x = memory.readfloat(0x8043A5E8)
    local y = memory.readfloat(0x8043A5EC)
    local z = memory.readfloat(0x8043A5F0)
    local rot = memory.readfloat(0x8043A5F4)
    local speed = memory.readfloat(0x8043A5F8)
    local item = memory.readbyte(0x8043A600)
    return {x, y, z, rot, speed, item}
end

local function readOpponents()
    local opponents = {}
    for i = 0, 3 do
        local x = memory.readfloat(0x80440000 + i*0x10)
        local y = memory.readfloat(0x80440004 + i*0x10)
        local z = memory.readfloat(0x80440008 + i*0x10)
        local speed = memory.readfloat(0x8044000C + i*0x10)
        local item = memory.readbyte(0x80440010 + i*0x10)
        table.insert(opponents, x)
        table.insert(opponents, y)
        table.insert(opponents, z)
        table.insert(opponents, speed)
        table.insert(opponents, item)
    end
    return opponents
end

local function setKartControls(action)
    local steer, gas, brake, useItem, drift, wheelie = unpack(action)
    joypad.set(1, {
        ["C-Stick X"] = steer * 100,
        ["A"] = gas,
        ["B"] = brake,
        ["Z"] = useItem,
        ["R"] = drift > 0 and true or false,
        ["L"] = wheelie > 0 and true or false
    })
end

while true do
    local state = readKartData()
    local opponents = readOpponents()
    for _, val in ipairs(opponents) do table.insert(state, val) end

    udp_send:sendto(table.concat(state, ","), host, port_send)

    local actionStr = udp_recv:receive()
    if actionStr then
        local action = {}
        for num in string.gmatch(actionStr, "[-]?%d+%.?%d*") do
            table.insert(action, tonumber(num))
        end
        setKartControls(action)
    end

    emu.frameadvance()
end
