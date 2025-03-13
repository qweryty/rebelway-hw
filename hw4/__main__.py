from tkinter import ttk, Tk

COLORS = ["red", "orange", "yellow", "green", "blue", "violet"]
COLUMNS = 5

if __name__ == "__main__":
    root = Tk()
    frame = ttk.Frame(root)
    frame.grid()
    ttk.Label(frame, text="Nobody will check it anyway").grid(column=0, row=0)
    style = ttk.Style()
    for i, color in enumerate(COLORS):
        style_name = f"{color}.TButton"
        style.configure(style_name, background=color)
        button = ttk.Button(frame, text="I am a button!", style=style_name)
        button.grid(column=0, row=i + 1)

    ttk.Label(frame, text="Now doing all the widgets")
    all_widgets_frame = ttk.Frame(frame)
    all_widgets_frame.grid()
    for i, widget in enumerate(ttk.__dict__.values()):
        if (
            not isinstance(widget, type)
            or not issubclass(widget, ttk.Widget)
            or widget is ttk.Widget
        ):
            continue

        try:
            widget(all_widgets_frame).grid(row=i // COLUMNS, column=i % COLUMNS)
        except TypeError:
            # Skipping hard to initialize widgets
            continue

    root.mainloop()
