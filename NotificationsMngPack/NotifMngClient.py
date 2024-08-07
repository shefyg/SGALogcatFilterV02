from abc import ABC, abstractmethod

class NotifMngClient(ABC):
    @abstractmethod
    def HandleNotif(self, notif_type, notif_info) -> None:
        '''

        :param notif_type: The key / type of notification
        :param notif_info: additional custom info if needed
        :return: None
        '''
        pass
