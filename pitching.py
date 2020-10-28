

def player_stats():
    from pybaseball import playerid_lookup
    from pybaseball import statcast_pitcher
    from pybaseball import pitching_stats
    
    first_name, last_name = input('Enter first and last name of player: ').split()
    full_name = str(first_name) + ' ' + str(last_name)
    
    info = playerid_lookup(str(last_name),str(first_name))
    refnum = int(info['key_mlbam'])
    debut_seas = str(int(info['mlb_played_first']))
    last_seas = str(int(info['mlb_played_last']))
    
    debut_yr = debut_seas + '-01-01'
    last_yr = last_seas + '-12-01'
    statcast = statcast_pitcher(debut_yr,last_yr,refnum)
    statcast.reset_index()
    
    reg_stat = pitching_stats(debut_seas,last_seas,qual=20)
    regular_stat = reg_stat[reg_stat['Name'] == full_name]

    return statcast, regular_stat

def pitch_breakdown(df):
    """returns an array with the layout for all pitches breakdown
    in the following way: strikes, balls, in play """


    """break df into years"""      
    if type(df) != list: 
        list_year = list(df['game_year'].unique())
        list_year.sort()
        yearly_df = list(map(lambda x: df[df['game_year'] == x], list_year))
    else:
        pass
    
    """yearly breakdown"""
    each_yr_pitch = []
    pitch_type_list_ref = [['swinging_strike','called_strike','foul','swinging_strike_blocked','missed_bunt','foul_tip','foul_bunt'],['ball','blocked_ball','pitchout','intent_ball'],['hit_into_play','hit_into_play_score','hit_into_play_no_out']]
    label_pitch = ['strike','ball','in play']
    
    """loop each year"""
    for yearly in yearly_df:
        
        pitch = []
        strike = []
        ball = []
        in_play = []
        
        """complete pitch breakdown"""
        for types in pitch_type_list_ref[0]:
            num = len(yearly[df['description'] == types])
            strike.append(num)
        for types in pitch_type_list_ref[1]:   
            num = len(yearly[df['description'] == types])
            ball.append(num) 
        for types in pitch_type_list_ref[2]:
            num = len(yearly[df['description'] == types])
            in_play.append(num)
            
        pitch.append(sum(strike))
        pitch.append(sum(ball))
        pitch.append(sum(in_play))
        
        each_yr_pitch.append(pitch)
        
    return each_yr_pitch


def strikeout_breakdown(df):
    """returns an array with the layout for all strikeout breakdown
    in the following way: called strikeout, swinging strikeout """

    """break df into years"""      
    if type(df) != list: 
        list_year = list(df['game_year'].unique())
        list_year.sort()
        yearly_df = list(map(lambda x: df[df['game_year'] == x], list_year))
    else:
        pass
    
    """yearly breakdown"""
    each_yr_so = []
    so_col = df['events'] == 'strikeout'
    label_so = ['called strikes', 'swinging strikes']
    
    for yearly in yearly_df:
        tot_so = []
        called = []
        swinging = []
        """strikeout breakdown"""
        called = len(yearly[so_col][df['description'] == 'called_strike'])
        swinging = len(yearly[so_col][df['description'] != 'called_strike'])
        tot_so.append(called)
        tot_so.append(swinging)
        each_yr_so.append(tot_so)
    
    return each_yr_so


def launch_angle_breakdown(df):
    """returns an array with the layout for all balls in play launch angle breakdown
    in the following way: ground ball, fly ball, line drive """
   
    """break df into years"""      
    if type(df) != list: 
        list_year = list(df['game_year'].unique())
        list_year.sort()
        yearly_df = list(map(lambda x: df[df['game_year'] == x], list_year))
    else:
        pass
    
    each_yr_inplay = []
    balls_in_play = ['hit_into_play','hit_into_play_score','hit_into_play_no_out']
    l_a = df['launch_angle']
    labels_la = ['GB/n(< 10)', 'FB/n(10 < x < 25)', 'LD/n(> 25)']
    
    for yearly in yearly_df:

        inplay = []
        grd_b = []
        line_d = []
        fly_b = []
        
        """balls in play launch angle breakdown"""
        for types in balls_in_play:
            num1 = len(yearly[df['description'] == types][l_a < 10.0])
            grd_b.append(num1)
            num2 = len(yearly[df['description'] == types][l_a >= 10.0][l_a <= 25.0])
            line_d.append(num2)
            num3 = len(yearly[df['description'] == types][l_a > 25.0])
            fly_b.append(num3)
        
        inplay.append(sum(grd_b))
        inplay.append(sum(fly_b))
        inplay.append(sum(line_d))
        
        each_yr_inplay.append(inplay)
        
    return each_yr_inplay


def exit_velocity_breakdown(df):
    """returns an array with the layout for all balls in play exit velocity breakdown
    in the following way: soft hit, medium hit, medium hit, hard hit"""
    
    """break df into years"""   
    if type(df) != list: 
        list_year = list(df['game_year'].unique())
        list_year.sort()
        yearly_df = list(map(lambda x: df[df['game_year'] == x], list_year))
    else:
        pass1
            
    each_yr_ev = []
    balls_in_play = ['hit_into_play','hit_into_play_score','hit_into_play_no_out']
    e_v = df['launch_speed']
    labels_ev = ['Soft Hit/n(< 75)', 'Mid Hit/n(75 < x < 85)', 'Mid Hit/n(85 < x < 95)', 'Hard Hit/n(>95)']
    
    for yearly in yearly_df:
        
        ev = []
        sft_h = []
        mid_h1 = []
        mid_h2 = []
        hrd_h = []
        
        """balls in play exit velo breakdown"""
        for types in balls_in_play:
            num1 = len(yearly[df['description'] == types][e_v < 75.0])
            sft_h.append(num1)
            num2 = len(yearly[df['description'] == types][e_v >= 75.0][e_v < 85.0])
            mid_h1.append(num2)
            num3 = len(yearly[df['description'] == types][e_v >= 85.0][e_v < 95.0])
            mid_h2.append(num3)
            num4 = len(yearly[df['description'] == types][e_v > 95.0])
            hrd_h.append(num4)
            
        ev.append(sum(sft_h))
        ev.append(sum(mid_h1))
        ev.append(sum(mid_h2))
        ev.append(sum(hrd_h))

        each_yr_ev.append(ev)

    return each_yr_ev

def graphing_pitching(df):

    """will take all the previous pitching breakdowns and compose pie charts of the values
    with the appropriate values"""
    import matplotlib.pyplot as plt

    list_year = list(df['game_year'].unique())
    list_year.sort()
    
    """all breakdowns"""
    player_name = df['player_name'].unique()[0]
    pitches = pitch_breakdown(df)
    strikeout  = strikeout_breakdown(df)
    launch_angle = launch_angle_breakdown(df)
    exit_velocity = exit_velocity_breakdown(df)
    
    """graphing all data"""
    
    for a, b, c, d, z in zip(pitches, strikeout, launch_angle, exit_velocity, list_year):
        plt.figure().suptitle(player_name + '\nBreakdown', fontsize='x-large',y=1.15)
        plt.subplot(2,2,1)
        plt.pie(a, labels=['strike','ball','in play'], autopct='%1.1f%%')
        plt.title(str(z) +' Pitch Breakdown')

        plt.subplot(2,2,2)
        plt.pie(b, labels=['called strikes', 'swinging strikes'], autopct='%1.1f%%')
        plt.title(str(z) + ' Strikeout Breakdown')

        if int(z) < 2015:
            pass

        else:
            plt.subplot(2,2,3)
            plt.pie(c, labels=['GB\n(< 10)', 'FB\n(> 25)', 'LD\n(10 < x < 25)'], autopct='%1.1f%%')
            plt.title(str(z) + ' Launch Angle (Degrees)')

            plt.subplot(2,2,4)
            plt.pie(d, labels=['Soft Hit\n(< 75)', 'Mid Hit\n(75 < x < 85)', 'Mid Hit\n(85 < x < 95)', 'Hard Hit\n(>95)'], autopct='%1.1f%%')
            plt.title(str(z) + ' Exit Velocity (MPH)')

        plt.tight_layout()
        plt.savefig('/Users/miguelgarcia/Desktop/baseball/graphs/' + player_name + ' ' + str(z) + '.pdf', bbox_inches='tight')
        plt.show()

        