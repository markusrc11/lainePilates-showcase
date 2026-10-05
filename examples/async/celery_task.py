from app.celery_app import celery_app


@celery_app.task
def send_reservation_confirmation(data: dict[str, str]) -> None:
    send_email(
        recipient=data["email"],
        template=data["template"],
        context=data,
    )
