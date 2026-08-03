# # Main implementation 
# try:
#     from gui_qt import gui as gui_qt
# except Exception:
#     gui_qt = None

# def main():
#     if gui_qt:
#         gui_qt()
#     else:
#         # Fallback: try the tkinter GUI if Qt is unavailable
#         from gui_new import gui as gui_tk
#         gui_tk()

# if __name__ == "__main__":
#     main()

def main():
    from gui_new import gui as gui_tk
    gui_tk()

if __name__ == "__main__":
    main()

