from windows_toasts import Toast, ToastDisplayImage, WindowsToaster

from modules.functions import resource_path

# show toast notification
def show_toast(message):
    toaster = WindowsToaster("Message-Client")

    toast = Toast()
    toast.text_fields = [message]

    # Bild hinzufügen (ToastImage mit einem ToastDisplayImage)
    image_path = resource_path("toast_logo.png")
    toast.AddImage(ToastDisplayImage.fromPath(image_path))

    toaster.show_toast(toast)