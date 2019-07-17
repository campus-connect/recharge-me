from django.utils import timezone
from django.db import IntegrityError
from celery import task
from celery.utils.log import get_task_logger
from accounts.models import Level, Peer, CustomUser

logger = get_task_logger(__name__)


@task(
    ignore_result=True
)
def peer_merging_task():

    for top_level in Level.objects.all().order_by('order'):
        print(top_level)
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
                            user_from=upline,
                            user_to=downline,
                            expires_at=timezone.now()
                        )
                    except IntegrityError:
                        continue
            else:
                logger.log(
                    msg="Breaking loop insufficient downlinesfor level {}\n".format(
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
