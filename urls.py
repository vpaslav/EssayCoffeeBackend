from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy

from django.contrib import admin
admin.autodiscover()

from tasks.views import CategoriesView, UpdateTaskView, CreateTaskView
from tasks.views import RemoveTaskView, DetailTaskView
from comments.views import CreateCommentView, RemoveCommentView
from general.views import LoginView, LogoutView, ResetPswdView
from general.views import ResetPswdDoneView, ResetPswdConfirmView, ResetPswdCompleteView

task_new = login_required(
    permission_required('tasks.add_task', raise_exception=True)(CreateTaskView.as_view()),
    login_url=reverse_lazy('login'))
task_update = login_required(
    permission_required('tasks.change_task', raise_exception=True)(UpdateTaskView.as_view()),
    login_url=reverse_lazy('login'))
task_rm = login_required(
    permission_required('tasks.delete_task', raise_exception=True)(RemoveTaskView.as_view()),
    login_url=reverse_lazy('login'))
task_details = DetailTaskView.as_view()

comment_new = login_required(
    permission_required('comments.add_comment', raise_exception=True)(CreateCommentView.as_view()),
    login_url=reverse_lazy('login'))
comment_rm = login_required(
    permission_required('comments.delete_comment', raise_exception=True)(RemoveCommentView.as_view()),
    login_url=reverse_lazy('login'))

urlpatterns = patterns('',
    url(r'^$', CategoriesView.as_view()),

    url(r'^category/(?P<category_id>\d{0,4})$', CategoriesView.as_view(), name='tasks_by_category'),

    url(r'^tasks/$', CategoriesView.as_view(), name='all_tasks'),
    url(r'^task/new$', task_new, name='task_new'),
    url(r'^task/(?P<pk>\d+)/$', task_details, name='task_view'),
    url(r'^task/(?P<pk>\d+)/edit$', task_update, name='task_edit'),
    url(r'^task/(?P<pk>\d+)/remove$', task_rm, name='task_remove'),

    url(r'^comment/(?P<task_id>\d+)/new$', comment_new, name='comment_new'),
    url(r'^comment/(?P<pk>\d+)/remove$', comment_rm, name='comment_remove'),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^reset/$', ResetPswdView.as_view(), name='pswd_reset'),
    url(r'^resetdone/$', ResetPswdDoneView.as_view(), name='pswd_reset_done'),
    url(r'^resetconfirm/(?P<uidb64>.*)/(?P<token>.*)$', ResetPswdConfirmView.as_view(), name='pswd_reset_confirm'),
    url(r'^resetcomplete/$', ResetPswdCompleteView.as_view(), name='pswd_reset_complete'),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^test/', BaseView.as_view(template_name='test/index.html'),{'module_path':'test'}),
)
