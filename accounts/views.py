#  * This file is part of recharge-me project.
#  * (c) Ochui Princewill Patrick <ochui.princewill@gmail.com>
#  * For the full copyright and license information, please view the "LICENSE.md"
#  * file that was distributed with this source code.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, ProcessFormView, FormMixin, FormView
from django.views.generic.list import ListView
from django.http import Http404
from django.urls import reverse
from django.contrib import messages
from allauth.account.models import EmailAddress
from notifications.signals import notify
from .models import CustomUser, Level, TransactionLog, Peer, Remerge
from .forms import EditProfileForm, LevelEnrollmentForm, ConfirmationForm
from . import verbs


class Dashboard(LoginRequiredMixin, TemplateView):

    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = 'dashboard'
        # check user email status
        # if not EmailAddress.objects.filter(user=self.request.user, verified=True).exists():
        #     context['verified_email'] = False
        # else:
        #     context['verified_email'] = True

        context['lastest_transactions'] = TransactionLog.objects.filter(
            user=self.request.user).order_by('-created')[:5]

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    template_name = "dashboard/profile.html"
    form_class = EditProfileForm
    model = CustomUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = 'profile'
        return context

    def get_object(self, queryset=None):
        """
        Returns a single user instance
        """
        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.filter(username=self.kwargs['username'])

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class LevelListView(LoginRequiredMixin, FormView):

    form_class = LevelEnrollmentForm
    template_name = "dashboard/level.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["level_list"] = Level.objects.all()
        context["page"] = 'level'
        return context

     # Hack to make request available in forms

    def get_form_kwargs(self):
        kw = super(LevelListView, self).get_form_kwargs()
        kw['request'] = self.request  # the trick!
        return kw

    def form_valid(self, form):
        if form.cleaned_data['action'] == 'enroll':
            form.enroll()
        else:
            form.un_enroll()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('level')


class PeerListView(LoginRequiredMixin, FormView, ListView):

    template_name = "dashboard/peer.html"
    context_object_name = 'peer_list'
    form_class = ConfirmationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "peer"
        return context

    def get_queryset(self):
        user = self.request.user
        if user.task == CustomUser.USER_TASK_RECEIVE_FUNDING:
            return user.followers.all()
        elif user.task == CustomUser.USER_TASK_SEND_FUNDING:
            return user.following.all()

    def get_form_kwargs(self):
        kw = super(PeerListView, self).get_form_kwargs()
        kw['request'] = self.request  # the trick!
        return kw

    def form_valid(self, form):
        if self.request.POST['action'] == 'confirm':
            # Delete relationship
            _user = CustomUser.objects.get(pk=form.cleaned_data['target'])
            _peer = Peer.objects.filter(user_from=_user).filter(
                user_to=self.request.user).delete()
            # Send Notification
            notify.send(
                sender=self.request.user, recipient=_user, verb=verbs.TRANSACTION_APPROVED_VERB,
                target=self.request.user, description=verbs.TRANSACTION_APPROVED_DESCRIPTION.format(
                    self.request.user)
            )
            # Log Transaction
            TransactionLog.objects.create(
                user=_user, amount=_user.level.entry_fee,
                status=TransactionLog.TRANSACTION_PAID,
                description=verbs.TRANSACTION_APPROVED_DESCRIPTION.format(
                    self.request.user)
            )
            # update user level
            _user.level = self.request.user.level
            _user.task = CustomUser.USER_TASK_RECEIVE_FUNDING
            _user.can_merge = True
            _user.save()

            _peer_count = Peer.objects.filter(
                user_to=self.request.user
            ).count()
            _peer_re_merge_count = Remerge.objects.filter(
                user=self.request.user
            ).count()
            if (_peer_count == 0) and (_peer_re_merge_count == 0):
                # update user Level/task
                r_user = CustomUser.objects.get(pk=self.request.user.id)
                next_level = None
                try:
                    next_level_order = self.request.user.level.order + 1
                    next_level = Level.objects.get(
                        order=next_level_order)
                    r_user.task = CustomUser.USER_TASK_SEND_FUNDING
                    r_user.can_merge = True
                    r_user.save()

                    # Send Notification
                    notify.send(
                        sender=self.request.user, recipient=self.request.user,  verb=verbs.NEW_LEVEL_VERB,
                        target=self.request.user, description=verbs.NEW_TASK
                    )
                except Level.DoesNotExist:
                    r_user.level = Level.objects.get(
                        order=1)  # Reset to level one
                    r_user.task = CustomUser.USER_TASK_SEND_FUNDING
                    r_user.can_merge = True
                    r_user.save()

                    # Send Notification
                    notify.send(
                        sender=self.request.user, recipient=self.request.user,  verb=verbs.NEW_LEVEL_VERB,
                        target=self.request.user, description=verbs.AUTO_SET_LEVEL.format(
                            r_user.level.name)
                    )
        elif self.request.POST['action'] == 'purge':
            # Penalize user reduce karma point
            # Delete Relationship
            _user = CustomUser.objects.get(pk=form.cleaned_data['target'])
            _peer = Peer.objects.filter(user_from=_user).filter(
                user_to=self.request.user).delete()
            # Re-merge User
            try:
                user_to_add = Remerge.objects.get(user=self.request.user)
                user_to_add.count = user_to_add.count + 1
                user_to_add.save()
            except Remerge.DoesNotExist:
                Remerge.objects.create(
                    user=self.request.user, level=self.request.user.level, count=1)
            # send Notification
            notify.send(
                sender=self.request.user, recipient=self.request.user, verb=verbs.PENDING_RE_MERGE_VERB,
                target=self.request.user, description=verbs.PENDING_RE_MERGE.format(
                    _user)
            )
            # Send Notification to defaulting user
            notify.send(
                sender=self.request.user, recipient=_user, verb=verbs.PURGE_VERB,
                target=self.request.user, description=verbs.PURGE.format(
                    self.request.user)
            )
            # Log Transaction
            TransactionLog.objects.create(
                user=_user, amount=_user.level.entry_fee,
                status=TransactionLog.TRANSACTION_REJECTED,
                description=verbs.PENDING_RE_MERGE.format(_user)
            )
        elif self.request.POST['action'] == 'purge_self':
            _user = CustomUser.objects.get(pk=form.cleaned_data['target'])
            # Delete Relationship
            _peer = Peer.objects.filter(user_from=self.request.user).filter(
                user_to=_user
            ).delete()
            # Re-merge User
            try:
                user_to_add = Remerge.objects.get(user=_user)
                user_to_add.count = user_to_add.count + 1
                user_to_add.save()
            except Remerge.DoesNotExist:
                Remerge.objects.create(
                    user=_user, level=_user.level, count=1)

             # send Notification
            notify.send(
                sender=self.request.user, recipient=_user, verb=verbs.PENDING_RE_MERGE_VERB,
                target=_user, description=verbs.PENDING_RE_MERGE.format(
                    _user)
            )
            notify.send(
                sender=self.request.user, recipient=self.request.user, verb=verbs.PURGE_VERB,
                target=_user, description=verbs.PURGE_SELF.format(
                    _user)
            )

        elif self.request.POST['action'] == 'paid':
            _user = CustomUser.objects.get(pk=form.cleaned_data['target'])
            # send Notification
            notify.send(
                sender=self.request.user, recipient=_user, verb=verbs.ATTENTION,
                target=_user, description=verbs.CONFIRMATION_REQUEST.format(
                    self.request.user)
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('peer')


class TransactionLogListView(LoginRequiredMixin, ListView):

    model = TransactionLog
    template_name = "dashboard/transaction.html"
    context_object_name = 'transaction_logs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "transaction"
        return context

    def get_queryset(self):

        filter = self.request.GET.get('filter')
        if filter:
            qs = TransactionLog.objects.filter(
                user=self.request.user,
            ).filter(status=filter)
        else:
            qs = TransactionLog.objects.filter(
                user=self.request.user,
            )

        return qs
