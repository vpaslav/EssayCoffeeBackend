from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy

from general.views import RemoveTaskView,SwitchStatusView
from general.views import CreateTaskView,UpdateTaskView,DetailTaskView,TaskIndexView
from general.models import Task
from comments.views import CreateCommentView,RemoveCommentView 

from userprofile.views import CreateProfileView, UpdateProfileView

import constants as co

task_rm = login_required(
    permission_required('general.delete_task', raise_exception=True)(RemoveTaskView.as_view()),
    login_url=reverse_lazy('login'))

comment_new = login_required(
    permission_required('comments.add_comment', raise_exception=True)
      (CreateCommentView.as_view(module_name='customer')),
    login_url=reverse_lazy('login'))
comment_rm = login_required(
    permission_required('comments.delete_comment', raise_exception=True)
      (RemoveCommentView.as_view(module_name='customer')),
    login_url=reverse_lazy('login'))


user_new = CreateProfileView.as_view(module_name='customer',
                                     group_name=co.CUSTOMER_GROUP)
user_edit = login_required(UpdateProfileView.as_view(module_name='customer'),
                           login_url=reverse_lazy('login'))

task_list = lambda request: login_required(
    TaskIndexView.as_view(module_name='customer', action_label='my orders',
                          queryset=Task.get_all_tasks(0, **{'owner__id': request.user.id})),
    login_url=reverse_lazy('login'))(request)
task_details = login_required(DetailTaskView.as_view(module_name='customer'),
                              login_url=reverse_lazy('login'))
task_new = login_required(
  permission_required('general.add_task', raise_exception=True)
    (CreateTaskView.as_view(module_name='customer')),
  login_url=reverse_lazy('login'))
task_status = login_required(
  permission_required('general.change_task', raise_exception=True)
    (SwitchStatusView.as_view(module_name='customer')),
  login_url=reverse_lazy('login'))
task_update = login_required(
  permission_required('general.change_task', raise_exception=True)
    (UpdateTaskView.as_view(module_name='customer')),
  login_url=reverse_lazy('login'))

urlpatterns = patterns('',
    url(r'^$', task_list),
    url(r'^tasks/$', task_list, name='task_list'),
    url(r'^task/(?P<pk>\d+)/$', task_details, name='task_view'),
    url(r'^task/(?P<pk>\d+)/remove$', task_rm, name='task_remove'),
    url(r'^task/new$', task_new, name='task_new'),
    url(r'^task/(?P<pk>\d+)/edit$', task_update, name='task_edit'),
    url(r'^task/(?P<pk>\d+)/status$', task_status, name='task_status'),

    url(r'^comment/(?P<task_id>\d+)/new$', comment_new, name='comment_new'),
    url(r'^comment/(?P<pk>\d+)/remove$', comment_rm, name='comment_remove'),

    url(r'profile/new', user_new, name='user_new'),
    url(r'profile/(?P<pk>\d+)/$', user_edit, name='user_details'),
    url(r'profile/(?P<pk>\d+)/edit$', user_edit, name='user_edit'),

    url(r'', include('common_urls')),
)

