class BaseballGrid(object):

    def __init__(self, x, y, goal):
        self.x = x
        self.y = y
        self.goal = goal

    def get_zone_index(self):

        if self.goal == "Location":
            lb, v1, v2, rb = -10, 20/3-10, 10-20/3, 10 # lb, v1, v2, v3, rb = -10, -5, 0, 5, 10
            tb, h1, h2 , bb = 42, 34, 26, 18 # tb, h1, h2 ,h3, bb = 42, 36, 30, 24, 18
            row = [lb, v1, v2, rb] # row = [lb, v1, v2, v3, rb]
            col = [tb, h1, h2 , bb] # col = [tb, h1, h2 ,h3, bb]
        elif self.goal == "Movement":
            v1, v2, v3 = -10, 0, 10
            h1, h2, h3 = -10, -20, -30
            row = [v1, v2, v3]
            col = [h1, h2, h3]
        elif self.goal == "Angle":
            v1, v2, v3 = -2.5, 0, 2.5
            h1, h2, h3 = -2.5, -5, -7.5
            row = [v1, v2, v3]
            col = [h1, h2, h3]

        # row index
        i = 0
        try:
            while self.x >= row[i]:
                i += 1
        except:
            i = len(row)
        row_index = i

        # column index
        k = 0
        try:
            while self.y <= col[k]:
                k += 1
        except:
            k = len(col)
        column_index = k

        # grid number
        grid_number = row_index + column_index*(len(row)+1)

        return grid_number


def heatmap(filename, goal, pitchtype, pitcherthrows, batterside):

    import numpy as np
    import pandas as pd
    import os
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    import matplotlib.patches as patches

    tm_data = pd.read_csv(os.path.join('uploads', filename), encoding='unicode_escape', index_col=False)

    # First step
    if batterside == 'Total':
        df_raw_1 = tm_data
    else:
        df_raw_1 = tm_data.loc[tm_data['BatterSide'] == batterside]

    if pitcherthrows == 'Total':
        df_raw_2 = df_raw_1
    else:
        df_raw_2 = df_raw_1.loc[df_raw_1['PitcherThrows'] == pitcherthrows]

    df_raw = df_raw_2

    # Second step
    ZoneIndex = []
    if goal == 'Location':
        df = df_raw.loc[df_raw['TaggedPitchType'] == pitchtype].dropna(subset=['PlateLocHeight', 'PlateLocSide'], how='any')
        for i in range(df.shape[0]):
            y = df['PlateLocHeight'].iloc[i]*12
            x = df['PlateLocSide'].iloc[i]*12
            ZoneIndex.append(BaseballGrid(x, y, 'Location').get_zone_index())
        df = df.assign(ZoneIndex=ZoneIndex)
        n = 25
    elif goal == 'Movement':
        df = df_raw.loc[df_raw['TaggedPitchType'] == pitchtype].dropna(subset=['VertBreak', 'HorzBreak'], how='any')
        for i in range(df.shape[0]):
            y = df['VertBreak'].iloc[i]
            x = df['HorzBreak'].iloc[i]
            ZoneIndex.append(BaseballGrid(x, y, 'Movement').get_zone_index())
        df = df.assign(ZoneIndex=ZoneIndex)
        n = 16
    elif goal == 'Angle':
        df = df_raw.loc[df_raw['TaggedPitchType'] == pitchtype].dropna(subset=['VertApprAngle', 'HorzApprAngle'], how='any')
        for i in range(df.shape[0]):
            y = df['VertApprAngle'].iloc[i]
            x = df['HorzApprAngle'].iloc[i]
            ZoneIndex.append(BaseballGrid(x, y, 'Angle').get_zone_index())
        df = df.assign(ZoneIndex=ZoneIndex)
        n = 16

    # Third step
    Probs_Dict = {'Number': [], 'Probs_1': [], 'Probs_2': [], 'Probs_3': [], 'Probs_4': [], 'Probs_5': [], 'Probs_6': [], 'Probs_7': [], 'Probs_8': [], 'Probs_9': []}
    total_pitches = df.shape[0]

    for zone in range(0, n):
        zone_data = df.loc[df['ZoneIndex'] == zone]
        zone_pitches = zone_data.shape[0]
        nonswing_pitches = zone_data.loc[(zone_data['PitchCall'] == 'BallCalled') | (zone_data['PitchCall'] == 'StrikeCalled')].shape[0]
        swing_pitches = zone_data.loc[(zone_data['PitchCall'] == 'StrikeSwinging') | (zone_data['PitchCall'] == 'FoulBall') | (zone_data['PitchCall'] == 'InPlay')].shape[0]
        inplay_pitches = zone_data.loc[zone_data['PitchCall'] == 'InPlay'].shape[0]

        hits = zone_data.loc[(zone_data['PlayResult'] == 'Single') | (zone_data['PlayResult'] == 'Double') | (zone_data['PlayResult'] == 'Triple') | (zone_data['PlayResult'] == 'Homerun')].shape[0]
        bases = zone_data.loc[zone_data['PlayResult'] == 'Single'].shape[0] + zone_data.loc[zone_data['PlayResult'] == 'Double'].shape[0]*2 + zone_data.loc[zone_data['PlayResult'] == 'Triple'].shape[0]*3 + zone_data.loc[zone_data['PlayResult'] == 'Homerun'].shape[0]*4
        balls = zone_data.loc[zone_data['PitchCall'] == 'BallCalled'].shape[0]
        strikes = zone_data.loc[zone_data['PitchCall'] == 'StrikeCalled'].shape[0]
        misses = zone_data.loc[zone_data['PitchCall'] == 'StrikeSwinging'].shape[0]
        groundballs = zone_data.loc[zone_data['HitType'] == 'GroundBall'].shape[0]
        popups = zone_data.loc[zone_data['HitType'] == 'Popup'].shape[0]
        # foulballs = zone_data.loc[zone_data['PitchCall'] == 'FoulBall'].shape[0]
        # foulballs_after_2strikes = zone_data.loc[(zone_data['PitchCall'] == 'FoulBall') & (zone_data['Strikes'] == 2)].shape[0]
        # outs = sum(zone_data.loc[(zone_data['PlayResult'] == 'Out') | (zone_data['PlayResult'] == 'FieldersChoice') | (zone_data['PlayResult'] == 'Sacrifice')]['OutsOnPlay'])

        prob1 = zone_pitches/total_pitches
        if zone_pitches == 0:
            prob2 = prob3 = prob4 = 0
        else:
            prob2 = hits/zone_pitches
            prob3 = bases/zone_pitches
            prob4 = swing_pitches/zone_pitches

        if swing_pitches == 0:
            prob5 = 0
        else:
            prob5 = misses/swing_pitches

        if inplay_pitches == 0:
            prob6 = prob7 = 0
        else:
            prob6 = groundballs/inplay_pitches
            prob7 = popups/inplay_pitches

        if nonswing_pitches == 0:
            prob8 = prob9 = 0
        else:
            prob8 = balls/nonswing_pitches
            prob9 = strikes/nonswing_pitches

        Probs_Dict['Number'].append(zone_pitches)
        Probs_Dict['Probs_1'].append(round(prob1*100, 2))
        Probs_Dict['Probs_2'].append(round(prob2*100, 2))
        Probs_Dict['Probs_3'].append(round(prob3, 2))
        Probs_Dict['Probs_4'].append(round(prob4*100, 2))
        Probs_Dict['Probs_5'].append(round(prob5*100, 2))
        Probs_Dict['Probs_6'].append(round(prob6*100, 2))
        Probs_Dict['Probs_7'].append(round(prob7*100, 2))
        Probs_Dict['Probs_8'].append(round(prob8*100, 2))
        Probs_Dict['Probs_9'].append(round(prob9*100, 2))

    #  Fourth step
    fig = Figure([16, 8])
    ax = fig.subplots(2, 5)
    # fig, ax = plt.subplots(2, 5, figsize=(16, 8))
    if goal == 'Location':
        for p_list in ax:
            for p in p_list:
                line = [(-10, 18), (-10, 42), (10, 42), (10, 18), (-10, 18)]
                path = patches.Polygon(line, facecolor='none', edgecolor='black', linewidth=2, closed=True, joinstyle='round')
                p.add_patch(path)
    else:
        pass

    if goal == 'Location':
        boundary = [-10-(20/3), 10+(20/3), 10, 50]
        matrix_shape = 5
    elif goal == 'Movement':
        boundary = [-20, 20, -40, 0]
        matrix_shape = 4
    elif goal == 'Angle':
        boundary = [-5, 5, -10, 0]
        matrix_shape = 4

    for m in range(2):
        for n in range(5):
            probs_dist = np.array(list(Probs_Dict.values())[n+m*5]).reshape(-1, matrix_shape)
            ax[m, n].imshow(probs_dist, cmap='coolwarm', extent=boundary)
            for i in range(matrix_shape):
                for j in range(matrix_shape):
                    if goal == 'Location':
                        ax[m, n].text((-10-(10/3))+(20/3)*j, 46-8*i, probs_dist[i, j], ha="center", va="center", size=9)
                    elif goal == 'Movement':
                        ax[m, n].text(-15+10*j, -5-10*i, probs_dist[i, j], ha="center", va="center", size=10)
                    elif goal == 'Angle':
                        ax[m, n].text(-3.75+2.5*j, -1.25-2.5*i, probs_dist[i, j], ha="center", va="center", size=10)

            if m == 0:
                if n == 0:
                    ax[m, n].set_title("Pitches")
                elif n == 1:
                    ax[m, n].set_title("Usage Percentage (%)")
                elif n == 2:
                    ax[m, n].set_title("Hits Percentage (%)")
                elif n == 3:
                    ax[m, n].set_title("Average Bases")
                elif n == 4:
                    ax[m, n].set_title("Swing Percentage (%)")
            elif m == 1:
                if n == 0:
                    ax[m, n].set_title("Swing&Misses Percentage (%)")
                elif n == 1:
                    ax[m, n].set_title("Groundballs Percentage (%)")
                elif n == 2:
                    ax[m, n].set_title("Popups Percentage (%)")
                elif n == 3:
                    ax[m, n].set_title("Balls Percentage (%)")
                elif n == 4:
                    ax[m, n].set_title("Strikes Percentage (%)")

    import io
    import base64
    save_file = io.BytesIO()
    fig.savefig(save_file, format='png')
    figdata_png = base64.b64encode(save_file.getvalue()).decode('utf8')

    return figdata_png

