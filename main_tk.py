import tkinter as tk
from tkinter import ttk

class Win11SearchWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Windows 11 Search")
        self.minsize(600, 400)
        self.configure(bg="#f0f0f0")
        self._build_ui()

    def _build_ui(self):
        # 主容器
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)

        # 搜索框
        search_frame = tk.Frame(main_frame, bg="white", bd=0, highlightthickness=0)
        search_frame.pack(fill=tk.X, pady=(0, 18))
        search_frame.pack_propagate(False)
        search_frame.configure(height=40)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("微软雅黑", 16), bd=0, relief=tk.FLAT)
        search_entry.insert(0, "在此键入以搜索")
        search_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 标签栏
        tab_names = ["All", "Apps", "Documents", "Web", "More"]
        self.tab_control = ttk.Notebook(main_frame)
        self.tabs = []
        for name in tab_names:
            frame = tk.Frame(self.tab_control, bg="#f0f0f0")
            self.tab_control.add(frame, text=name)
            self.tabs.append(frame)
        self.tab_control.pack(fill=tk.BOTH, expand=False)
        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # 内容区
        self._build_all_tab(self.tabs[0])
        self._build_simple_tab(self.tabs[1], "Apps Page Content")
        self._build_simple_tab(self.tabs[2], "Documents Page Content")
        self._build_simple_tab(self.tabs[3], "Web Page Content")
        self._build_simple_tab(self.tabs[4], "More Page Content")

    def _build_all_tab(self, parent):
        # 使用 grid 重新布局，确保所有分区完整显示且自适应
        parent.grid_rowconfigure(0, weight=0)
        parent.grid_rowconfigure(1, weight=0)
        parent.grid_rowconfigure(2, weight=0)
        parent.grid_rowconfigure(3, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Top apps 区域
        top_label = tk.Label(parent, text="Top apps", font=("微软雅黑", 16, "bold"), bg="#f0f0f0")
        top_label.grid(row=0, column=0, sticky="w", pady=(10, 0))
        apps_frame = tk.Frame(parent, bg="#f0f0f0")
        apps_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        apps = [
            ("File Explorer", "#0078d4"),
            ("Settings", "#50e6ff"),
            ("Control Panel", "#8764b8"),
            ("Microsoft Store", "#107c10"),
            ("Groove Music", "#e81123")
        ]
        for idx, (app_name, color) in enumerate(apps):
            btn = tk.Frame(apps_frame, width=120, height=120, bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
            btn.grid(row=0, column=idx, padx=8, pady=8)
            btn.pack_propagate(False)
            color_block = tk.Label(btn, bg=color, width=6, height=3)
            color_block.pack(pady=(18, 8))
            label = tk.Label(btn, text=app_name, font=("微软雅黑", 13), bg="white")
            label.pack()
        # Recent 区域
        recent_label = tk.Label(parent, text="Recent", font=("微软雅黑", 15, "bold"), bg="#f0f0f0")
        recent_label.grid(row=2, column=0, sticky="w", pady=(18, 6))
        recent_items = ["Registry Editor", "Run", "Control Panel", "Windows PowerShell"]
        recent_frame = tk.Frame(parent, bg="#f0f0f0")
        recent_frame.grid(row=3, column=0, sticky="ew")
        for i, item in enumerate(recent_items):
            btn = tk.Button(recent_frame, text=item, anchor="w", font=("微软雅黑", 14), bg="white", relief=tk.FLAT, bd=0, highlightthickness=0)
            btn.grid(row=i//2, column=i%2, sticky="ew", padx=6, pady=3, ipadx=10, ipady=6)
        # Quick searches 区域
        quick_label = tk.Label(parent, text="Quick searches", font=("微软雅黑", 15, "bold"), bg="#f0f0f0")
        quick_label.grid(row=4, column=0, sticky="w", pady=(18, 6))
        quick_items = ["Weather", "Top news", "Today in history", "Coronavirus tips"]
        quick_frame = tk.Frame(parent, bg="#f0f0f0")
        quick_frame.grid(row=5, column=0, sticky="ew")
        for i, item in enumerate(quick_items):
            btn = tk.Button(quick_frame, text=item, anchor="w", font=("微软雅黑", 14), bg="white", relief=tk.FLAT, bd=0, highlightthickness=0)
            btn.grid(row=i//2, column=i%2, sticky="ew", padx=6, pady=3, ipadx=10, ipady=6)
        # 让 recent_frame 和 quick_frame 可扩展
        recent_frame.grid_columnconfigure(0, weight=1)
        recent_frame.grid_columnconfigure(1, weight=1)
        quick_frame.grid_columnconfigure(0, weight=1)
        quick_frame.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(6, weight=1)

    def _build_simple_tab(self, parent, text):
        label = tk.Label(parent, text=text, font=("微软雅黑", 15), bg="#f0f0f0")
        label.pack(pady=40)

    def on_tab_changed(self, event):
        pass

if __name__ == "__main__":
    app = Win11SearchWindow()
    app.mainloop()