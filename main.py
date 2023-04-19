import tkinter as tk
from tkinter import ttk
from search import search_places
import webbrowser

# 每頁呈現的結果數量
display_count = 10

def show_results():
    global start, page, total_pages
    
    text.delete('1.0', tk.END)
    for i in range(start, start + display_count):
        if i >= len(results):
            break
        result = results[i]
        text.insert(tk.END, f"{result['name']}\n")
        text.insert(tk.END, f"{result['address']}\n")
        text.insert(tk.END, f"評分: {result['rating']}\n")
        # 地圖開啟按鈕
        button = ttk.Button(text, text="打開地圖查看", command=lambda loc=result['location']: show_map(loc))
        text.window_create(tk.END, window=button)
        text.insert(tk.END, "\n\n")

    pages_label.config(text=f"第 {page+1} 頁 / 共 {total_pages} 頁")
    scrollbar.config(command=text.yview)
    text.config(yscrollcommand=scrollbar.set)
def search():
    area = entry.get()
    global results, start, page, total_pages
    
    results = search_places(area)
    start = 0
    page = 0
    total_pages = (len(results) - 1) // display_count + 1
    show_results()



def show_map(location):
    url = f"https://www.google.com.tw/maps/place/{location['lat']},{location['lng']}"
    webbrowser.open_new_tab(url)

def open_result_info():
    selection = text.tag_ranges(tk.SEL)
    if selection:
        index1 = text.index(tk.SEL_FIRST)
        index2 = text.index(tk.SEL_LAST)
        name = text.get(index1, index2).split("\n")[0]
        for result in results:
            if result['name'] == name:
                place_id = result['place_id']
                url = (f"https://maps.googleapis.com/maps/api/place/details/json?place_id=PLACE_ID&fields=name,rating,formatted_address&key=AIzaSyCJxyreN2bQmxOgYTLL-BqcAVXNnA714jY")
                webbrowser.open(url)
                

def next_page():
    global page, start
    if page < total_pages - 1:
        page += 1
        start += display_count
        show_results()

def prev_page():
    global page, start
    if page > 0:
        page -= 1
        start -= display_count
        show_results()

window = tk.Tk()
window.geometry("1000x800")
window.title("餐廳搜尋系統")

style = ttk.Style(window)
style.theme_use("clam")
style.configure(".", font=("Helvetica", 12))
style.configure("TLabel", foreground="black", background="white")
style.configure("TButton", foreground="white", background="#0078d7")
style.map("TButton", background=[("active", "#0065a0")])

label = ttk.Label(window, text="請輸入地區：")
label.pack(pady=10)

entry = ttk.Entry(window, width=20, font=("Helvetica", 12))
entry.pack(pady=10)

button = ttk.Button(window, text="搜尋", command=search)
button.pack(pady=10)

map_frame = ttk.Frame(window)
map_frame.pack(pady=10, fill=tk.BOTH, expand=True)

map_label = ttk.Label(map_frame, text="地圖顯示區")
map_label.pack(pady=10)

frame = ttk.Frame(window)
frame.pack(pady=10, fill=tk.BOTH, expand=True)

text = tk.Text(frame, height=20, font=("Helvetica", 12))
text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

pages_label = ttk.Label(window, text="")
pages_label.pack(pady=10)

prev_button = ttk.Button(window, text="上一頁", command=prev_page)
prev_button.pack(side=tk.LEFT, padx=10)

next_button = ttk.Button(window, text="下一頁", command=next_page)
next_button.pack(side=tk.RIGHT, padx=10)

window.mainloop()