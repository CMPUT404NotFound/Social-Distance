


from corsheaders.signals import check_request_enabled

def corsStuff(sender, request, **kwargs):
    print("testing", sender, request, kwargs)
    return False


check_request_enabled.connect(corsStuff)

