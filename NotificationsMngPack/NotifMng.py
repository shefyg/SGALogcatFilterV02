import threading


class NotifMng:

    instance = None

    def __init__(self):
        if NotifMng.instance is not None:
            raise Exception("This class is a singleton!")
        self.notifType2clients = {}
        NotifMng.instance = self

    @staticmethod
    def get_instance():
        if NotifMng.instance is None:
            NotifMng.instance = NotifMng()
        return NotifMng.instance

    @staticmethod
    def register_client(notif_type, client):
        nm = NotifMng.get_instance()
        if notif_type not in nm.notifType2clients:
            nm.notifType2clients[notif_type] = []
        nm.notifType2clients[notif_type].append(client)

    @staticmethod
    def notify(notif_type, notif_info, delay=0):
        if delay and delay > 0:
            timer = threading.Timer(delay, NotifMng.notify_clients, args=(notif_type, notif_info))
            timer.start()
        else:
            NotifMng.notify_clients(notif_type, notif_info)

    @staticmethod
    def notify_clients(notif_type, notif_info):
        nm = NotifMng.get_instance()
        if notif_type in nm.notifType2clients:
            for client in nm.notifType2clients[notif_type]:
                client.HandleNotif(notif_type, notif_info)
        else:
            print(f"No clients registered for notification type: {notif_type}")
