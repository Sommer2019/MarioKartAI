import socket, numpy as np, time, os
from agent import PPOAgent
from strategy import high_level_strategy
from stats_plot import plot_stats

# File-based communication for compatibility with Dolphin Lua
SEND_FILE = "python_to_lua.txt"
RECV_FILE = "lua_to_python.txt"

# Initialize communication files
with open(SEND_FILE, "w") as f:
    f.write("")
with open(RECV_FILE, "w") as f:
    f.write("")

agent = PPOAgent()
prev_state = np.zeros(26)
offroad_counter = 0
log_data = {"frame":[],"speed":[],"drift":[],"wheelie":[],"offroad":[],"reward":[],"items_used":[],"overtakes":[],"crashes":[],"lost_races":[]}
frame_count = 0

def get_reward(state, prev_state, offroad_counter):
    reward=state[0]-prev_state[0]
    for i in range(6,len(state),5):
        if state[0]>prev_state[i] and prev_state[0]<=prev_state[i]: reward+=10
    if state[5]>0 and state[4]>prev_state[4]: reward+=10
    for i in range(9,len(state),5):
        if state[i]==3: reward-=5
    drift_flag = state[7] if len(state)>7 else 0
    wheelie_flag = state[8] if len(state)>8 else 0
    speed = state[4]; rot = state[3]
    if abs(rot)>0.2 and drift_flag: reward+=0.3
    if abs(rot)<0.05 and wheelie_flag and speed>3: reward+=0.1
    if state[1]<-5 or state[1]>5: reward-=50; log_data["crashes"].append(1)
    if state[0]>1000: reward+=100
    offroad_threshold=-1; speed_threshold=3; offroad_limit=20
    if state[1]<offroad_threshold and speed<speed_threshold:
        offroad_counter+=1
        if offroad_counter>offroad_limit: reward-=5
    else: offroad_counter=0
    return reward, offroad_counter

def read_from_lua():
    """Read data from Lua script via file"""
    try:
        if os.path.exists(RECV_FILE):
            with open(RECV_FILE, "r") as f:
                data = f.read().strip()
            if data:
                # Clear file after reading
                with open(RECV_FILE, "w") as f:
                    f.write("")
                return data
    except (IOError, OSError):
        pass
    return None

def send_to_lua(data):
    """Send data to Lua script via file"""
    try:
        with open(SEND_FILE, "w") as f:
            f.write(data)
        return True
    except (IOError, OSError):
        return False

while True:
    frame_count+=1
    try:
        data_str = read_from_lua()
        if data_str:
            state=np.array([float(x) for x in data_str.split(",")])
            use_item_flag, drift_flag, wheelie_flag = high_level_strategy(state)
            action = agent.select_action(state)
            action[3]=use_item_flag; action[4]=drift_flag; action[5]=wheelie_flag
            reward, offroad_counter = get_reward(state, prev_state, offroad_counter)
            agent.store_transition(state, action, reward)
            agent.train_if_ready()
            prev_state=state.copy()
            log_data["frame"].append(frame_count); log_data["speed"].append(state[4]); log_data["drift"].append(drift_flag)
            log_data["wheelie"].append(wheelie_flag); log_data["offroad"].append(int(state[1]<-1))
            log_data["reward"].append(reward); log_data["items_used"].append(use_item_flag)
            action_str=",".join([str(a) for a in action])
            send_to_lua(action_str)
    except (ValueError, IndexError):
        pass
    time.sleep(0.01)
