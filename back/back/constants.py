import os


def values(request):
    return {
        'FA_KIT_ID': os.environ.get("FA_KIT_ID")
    }
