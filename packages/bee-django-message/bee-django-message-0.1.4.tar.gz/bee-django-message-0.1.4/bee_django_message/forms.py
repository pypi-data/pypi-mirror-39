#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bee'

from django import forms
from .models import Message,SendRecord


# ===== course contract======
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['identity','name', "info", "is_user_show", "is_admin_show",'is_done',"is_replay"]

class RecordChangeDoneForm(forms.ModelForm):
    class Meta:
        model = SendRecord
        fields = ['done_info']