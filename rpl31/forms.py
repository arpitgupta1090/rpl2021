from django import forms
from rpl31.models import RplUsers, Selected
from rpl31.config import Envariable
from rpl31.formatdata import getSeries, getMatch

'''
#plist = [('a','b'),('c','d'),('e','f')]
#matchid = 123
#matchdesc = 'Temp match'
#mlist = [(1,'b'),(2,'d'),(3,'f')]'''


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = RplUsers
        fields = ['UserName', 'emailId', 'mobile', 'pwd']
        widgets = {'pwd': forms.PasswordInput(), }
        labels = {'pwd': 'Password', }

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("pwd")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password and password:
            raise forms.ValidationError("password and confirm_password does not match")
        return cleaned_data


class LoginForm(forms.ModelForm):

    class Meta:
        model = RplUsers
        fields = ['emailId', 'pwd']
        widgets = {'pwd': forms.PasswordInput(), }
        labels = {'pwd': 'Password', }

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get("emailId")
        password = cleaned_data.get("pwd")

        user = RplUsers.objects.get(emailId=email)
        if user.pwd != password:
            raise forms.ValidationError("Invalid password")
        if not user.activeflag:
            raise forms.ValidationError("User is not active, please contact admin")

        return cleaned_data


class SelectModelForm(forms.ModelForm):
    matchDesc = forms.CharField(max_length=100, label="Match", disabled=True)

    def __init__(self, *args, **kwargs):
        sid = Envariable().sid
        match_id, match_desc, plist = getSeries(sid, 'live')
        super(SelectModelForm, self).__init__(*args, **kwargs)
        self.fields['seriesId'].initial = sid
        self.fields['matchId'].initial = match_id
        self.fields['matchDesc'].initial = match_desc
        self.fields['player1'] = forms.ChoiceField(choices=plist)
        self.fields['player2'] = forms.ChoiceField(choices=plist)
        self.fields['player3'] = forms.ChoiceField(choices=plist)
        self.fields['player4'] = forms.ChoiceField(choices=plist)
        self.fields['player5'] = forms.ChoiceField(choices=plist)

    class Meta:
        model = Selected
        fields = ['matchDesc', 'matchId', 'player1', 'player2', 'player3', 'player4', 'player5', 'seriesId', 'userName']
        widgets = {'matchId': forms.HiddenInput(), 'seriesId': forms.HiddenInput(), 'userName': forms.HiddenInput(), }

    def clean(self):
        cleaned_data = super(SelectModelForm, self).clean()
        player1 = cleaned_data.get("player1")
        player2 = cleaned_data.get("player2")
        player3 = cleaned_data.get("player3")
        player4 = cleaned_data.get("player4")
        player5 = cleaned_data.get("player5")
        match_id = cleaned_data.get("matchId")
        status = getMatch(match_id, 'status')
        select1status = Envariable().select1status

        if player5 == player1 or player5 == player2:
            raise forms.ValidationError("Batsman and All-rounder can't be same")
        elif player1 == player2:
            raise forms.ValidationError("Both batsmen can't be same")
        elif player5 == player3 or player5 == player4:
            raise forms.ValidationError("Bowler and All-rounder can't be same")
        elif player3 == player4:
            raise forms.ValidationError("Both Bowlers can't be same")

        if status not in select1status:
            raise forms.ValidationError("Match Already started")

        return cleaned_data


class SelectForm(forms.Form):

    def __init__(self, *args, **kwargs):
        sid = Envariable().sid
        match_id, match_desc, plist = getSeries(sid, 'live')
        super(SelectForm, self).__init__(*args, **kwargs)
        self.fields['matchid'].initial = match_id
        self.fields['matchdesc'].initial = match_desc
        self.fields['player1'].choices = plist
        self.fields['player2'].choices = plist
        self.fields['player3'].choices = plist
        self.fields['player4'].choices = plist
        self.fields['player5'].choices = plist

    matchid = forms.DecimalField(widget=forms.HiddenInput())
    matchdesc = forms.CharField(label='Match', disabled=True, widget=forms.Textarea(attrs={'cols': 40, 'rows': 3}))
    player1 = forms.ChoiceField(label='Select 1st Batsman')
    player2 = forms.ChoiceField(label='Select 2nd Batsman')
    player3 = forms.ChoiceField(label='Select 1st Bowler')
    player4 = forms.ChoiceField(label='Select 2nd Bowler')
    player5 = forms.ChoiceField(label='Select All-rounder')


class ScoreForm(forms.Form):

    def __init__(self, *args, **kwargs):
        sid = Envariable().sid
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.fields['matchid'].choices = getSeries(sid, 'past')

    matchid = forms.ChoiceField(label='Select match')


class UploadForm(forms.ModelForm):
    class Meta:
        model = RplUsers
        fields = ['image']


class UpdateForm(forms.ModelForm):
    class Meta:
        model = RplUsers
        fields = ('emailId', 'mobile')
        labels = {'emailId': 'Enter your Email-Id', }


class PassForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = RplUsers
        fields = ['pwd']
        widgets = {'pwd': forms.PasswordInput(), }
        labels = {'pwd': 'Current Password', }

    def clean(self):
        cleaned_data = super(PassForm, self).clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password and password:
            raise forms.ValidationError("password and confirm_password does not match")
        return cleaned_data


class OtpForm(forms.Form):
    UserName = forms.CharField(label="Email or User name")
    otp = forms.DecimalField(required=False, widget=forms.Textarea(attrs={'cols': 6, 'rows': 1}))
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)
