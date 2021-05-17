from win10toast import ToastNotifier


class Notifier:
    @staticmethod
    def Notify(vaccins: list) -> None:
        text = '\n'.join(vaccins)

        n = ToastNotifier()
        n.show_toast(
            title="{} vaccins gevonden!\n".format(len(vaccins)),
            msg=text,
            icon_path='./Spuit.ico',
            duration=10,
            threaded=True
        )
