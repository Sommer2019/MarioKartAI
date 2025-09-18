import socket, numpy as np, time
from agent import PPOAgent
from strategy import high_level_strategy
from stats_plot import plot_stats

udp_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_recv.bind(("127.0.0.1",12345)); udp_recv.settimeout(0.001)
udp_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

while True:
    frame_count+=1
    try:
        data,_=udp_recv.recvfrom(1024)
        state=np.array([float(x) for x in data.decode().split(",")])
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
        udp_send.sendto(action_str.encode(),("127.0.0.1",12346))
    except socket.timeout: pass
    time.sleep(0.01)
