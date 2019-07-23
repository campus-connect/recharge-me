from datetime import timedelta
from django.utils import timezone
from django.db import IntegrityError
from celery import task
from celery.utils.log import get_task_logger
from notifications.signals import notify
from accounts.models import Level, Peer, CustomUser, Remerge
from accounts import verbs
from recharge.utils import humanizer

logger = get_task_logger(__name__)


@task(
    ignore_result=True
)
def peer_merging_task():

    for top_level in Level.objects.all().order_by('order'):
        # get buttom level for current top_level
        buttom_level = None
        try:
            buttom_level_order = (top_level.order-1)
            buttom_level = Level.objects.get(order=buttom_level_order)
        except Level.DoesNotExist:
            logger.log(
                msg="Breaking loop Level with the order of {} does not exist\n".format(
                    buttom_level_order
                ),
                level=20)
            continue

        upline_user_list = CustomUser.objects.filter(
            task=CustomUser.USER_TASK_RECEIVE_FUNDING,
            level=top_level
        )

        for upline in upline_user_list:
            downline_user_list = CustomUser.objects.filter(
                task=CustomUser.USER_TASK_SEND_FUNDING,
                level=buttom_level
            )[:2]

            if downline_user_list.count() > 1:
                for downline in downline_user_list:
                    try:
                        Peer.objects.create(
                            user_from=downline,
                            user_to=upline,
                            expires_at=timezone.now() + timedelta(hours=2)  # Two hours from now
                        )
                        notify.send(
                            sender=downline, recipient=downline, verb=verbs.NEW_TASK,
                            target=upline, description=verbs.MERGED_TASK_SEND.format(
                                upline)
                        )
                    except IntegrityError:
                        continue
                notify.send(
                    sender=upline, recipient=upline, verb=verbs.MERGED_TASK_RECEIVED_VERB,
                    description=verbs.MERGED_TASK_RECEIVED.format(
                        humanizer.humanize_list(downline_user_list))
                )
            else:
                logger.log(
                    msg="Breaking loop insufficient downlines for level {}\n".format(
                        top_level
                    ),
                    level=20
                )
                break
        else:
            logger.log(
                msg="Breaking loop insufficient uplines for level {}\n".format(
                    top_level
                ),
                level=20
            )
            break


@task(
    ignore_result=True
)
def peer_re_merging_task():
    
    uplines = Remerge.objects.all()
    for upline in uplines:
        # get buttom level for current top_level
        buttom_level = None
        try:
            buttom_level_order = (upline.level.order-1)
            buttom_level = Level.objects.get(order=buttom_level_order)
        except Level.DoesNotExist:
            logger.log(
                msg="Breaking loop Level with the order of {} does not exist\n".format(
                    buttom_level_order
                ),
                level=20)
            continue
        
        downline_user_list = CustomUser.objects.filter(
                task=CustomUser.USER_TASK_SEND_FUNDING,
                level=buttom_level
            )[:upline.count]
        

        if downline_user_list.count() > 0:
            for downline in downline_user_list:
                try:
                    Peer.objects.create(
                        user_from=downline,
                        user_to=upline.user,
                        expires_at=timezone.now() + timedelta(hours=2)  # Two hours from now
                    )
                    notify.send(
                        sender=downline, recipient=downline, verb=verbs.NEW_TASK,
                        target=upline, description=verbs.MERGED_TASK_SEND.format(
                            upline)
                    )
                    upline.count = upline.count - 1
                    upline.save()
                    if upline.count == 0:
                        upline.delete() 
                except IntegrityError:
                    continue
            notify.send(
                sender=upline.user, recipient=upline.user, verb=verbs.MERGED_TASK_RECEIVED_VERB,
                description=verbs.MERGED_TASK_RECEIVED.format(
                    humanizer.humanize_list(downline_user_list))
            )
        else:
            logger.log(
                msg="Breaking loop insufficient downlines for level {}\n".format(
                    upline.level
                ),
                level=20
            )
            continue # Check next user