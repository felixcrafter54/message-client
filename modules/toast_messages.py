from windows_toasts import ToastDisplayImage, ToastImageAndText4, WindowsToaster

from modules.functions import resource_path

# show toast notification
def show_toast(message):
    toaster = WindowsToaster("Windows-Toasts")
    new_toast = ToastImageAndText4()
    new_toast.SetBody(message)
    # Hier kannst du den Pfad zu deinem eigenen Bild angeben
    new_toast.AddImage(ToastDisplayImage.fromPath(resource_path("toast_logo.png")))
    toaster.show_toast(new_toast)

#def show_toast(message,)