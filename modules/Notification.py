from plyer import notification


def notify(message, title="Error"):
    notification.notify(
        title=title,
        message=message,
        app_icon="icons/icon.ico",
        timeout=2,
    )
