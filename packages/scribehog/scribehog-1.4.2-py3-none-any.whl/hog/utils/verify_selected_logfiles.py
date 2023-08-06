def verify_selected_logfiles() -> bool:
    reply = input("---hog Do you want to print these files? [Y/n]  ")
    return reply.upper() == "Y"
