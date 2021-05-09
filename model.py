from wtforms import Form, FileField, SelectField, validators

class InputForm(Form):

    FileName = FileField(
        label='TrackMan:',
        validators=[validators.InputRequired()]
        )
    Goal = SelectField(
        label='Goal:',
        # choices is (value, label) pairs: label gets printed
        # value is form.Goal.data
        choices=[('Location', 'Location'),
                 ('Movement', 'Movement'),
                 ('Angle', 'Angle')],
        default=3
        )
    PitchType = SelectField(
        label='PitchType:',
        # choices is (value, label) pairs: label gets printed
        # value is form.PitchType.data
        choices=[('Fastball', 'Fastball'),
                 ('Splitter', 'Splitter'),
                 ('ChangeUp', 'ChangeUp'),
                 ('Slider', 'Slider'),
                 ('Curveball', 'Curveball'),
                 ('Sinker', 'Sinker'),
                 ('Cutter', 'Cutter'),
                 ('KnuckleBall', 'KnuckleBall')],
        default=8
        )
    PitcherThrows = SelectField(
        label='PitcherThrows:',
        # choices is (value, label) pairs: label gets printed
        # value is form.PitcherThrows.data
        choices=[('Right', 'Right'),
                 ('Left', 'Left'),
                 ('Total', 'Total')],
        default=3
        )
    BatterSide = SelectField(
        label='BatterSide:',
        # choices is (value, label) pairs: label gets printed
        # value is form.BatterSide.data
        choices=[('Right', 'Right'),
                 ('Left', 'Left'),
                 ('Total', 'Total')],
        default=3
        )
