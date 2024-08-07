
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
    def notify(notif_type, notif_info):
        nm = NotifMng.get_instance()
        if notif_type in nm.notifType2clients:
            for client in nm.notifType2clients[notif_type]:
                client.HandleNotif(notif_type, notif_info)
        else:
            print(f"No clients registered for notification type: {notif_type}")