from django import forms
from django.core.exceptions import ValidationError


#定义一个注册的form类
class RegForm(forms.Form):
    username=forms.CharField(max_length=12,
                             label='用户名',
                             error_messages={'max_length':'用户名最长为12位',
                                             'required':'用户名不能为空'},
                             widget=forms.widgets.TextInput(attrs={'class':'form-control'}))

    password = forms.CharField(
        min_length=6,
        label="密码",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"},
            render_value=True,
        ),
        error_messages={
            "min_length": "密码至少要6位！",
            "required": "密码不能为空",
        }
    )

    re_password = forms.CharField(
        min_length=6,
        label="确认密码",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"},
            render_value=True,
        ),
        error_messages={
            "min_length": "确认密码至少要6位！",
            "required": "确认密码不能为空",
        }
    )

    email = forms.EmailField(
        label="邮箱",
        widget=forms.widgets.EmailInput(
            attrs={"class": "form-control"},

        ),
        error_messages={
            "invalid": "邮箱格式不正确！",
            "required": "邮箱不能为空",
        }
    )

    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")

        if re_password and re_password != password:
            self.add_error("re_password", ValidationError("两次密码不一致"))

        else:
            return self.cleaned_data
