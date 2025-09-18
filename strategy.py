def high_level_strategy(state):
    use_item=0
    drift_flag=0
    wheelie_flag=0
    my_item=state[5]
    my_rot=state[3]
    my_speed=state[4]
    my_x=state[0]
    for i in range(6,len(state),5):
        opponent_x = state[i]
        if my_item>0 and (opponent_x-my_x)<5:
            use_item=1
            break
    if abs(my_rot)>0.2: drift_flag=1
    if abs(my_rot)<0.05 and drift_flag==0 and my_speed>3: wheelie_flag=1
    return use_item, drift_flag, wheelie_flag