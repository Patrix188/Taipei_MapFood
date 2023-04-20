import tkinter as tk
from tkinter import ttk
from search import search_places
import googlemaps
import webbrowser

API_KEY = 'AIzaSyCJxyreN2bQmxOgYTLL-BqcAVXNnA714jY'
gmaps = googlemaps.Client(key=API_KEY)

# 每頁呈現的結果數量
display_count = 5

def show_results():
    global start, page, total_pages
    
    tree.delete(*tree.get_children())
    for i in range(start, start + display_count):
        if i >= len(results):
            break
        result = results[i]
        tree.insert("", tk.END, values=(result['name'], result['address'], result['rating']))
    
    pages_label.config(text=f"第 {page+1} 頁 / 共 {total_pages} 頁")

def search():
    global results, start, page, total_pages
    
    area = entry.get()
    results = search_places(area)
    start = 0
    page = 0
    total_pages = (len(results) - 1) // display_count + 1
    show_results()

def show_map(location):
    results = search_places(location)
    if len(results) == 0:
        print('No results found.')
        return
    # 取得第一個搜尋結果的地點
    location = results[0]['location']
    # 組合 Google Maps API 的查詢字串
    query = f"https://www.google.com/maps/search/?api=1&query={location['lat']},{location['lng']}"
    # 開啟瀏覽器顯示地圖
    webbrowser.open(query)

def open_result_info():
    selection = tree.selection()
    if selection:
        item = tree.item(selection[0])
        name = item['values'][0]
        for result in results:
            if result['name'] == name:
                place_id = result['place_id']
                webbrowser.open(f"https://www.google.com.tw/maps/place/?q=place_id:{place_id}")
                break
#上下頁
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

#建立主視窗
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

map_label = ttk.Label(map_frame, text="圖片參考")
map_label.pack(pady=10)

frame = ttk.Frame(window)
frame.pack(pady=10, fill=tk.BOTH, expand=True)

tree = ttk.Treeview(frame, columns=("Name", "Address", "Rating"), show="headings")
tree.heading("Name", text="店名")
tree.heading("Address", text="地址")
tree.heading("Rating", text="評分")
tree.column("Name", width=200)
tree.column("Address", width=400)
tree.column("Rating", width=50)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree.configure(yscrollcommand=scrollbar.set)

pages_label = ttk.Label(window, text="")
pages_label.pack(pady=10)

location_entry = tk.Entry(window)
location_entry.pack(side=tk.LEFT)

map_button = tk.Button(window, text="打開地圖查看", command=lambda: show_map(location_entry.get()))
map_button.pack(side=tk.RIGHT)

prev_button = ttk.Button(window, text="上一頁", command=prev_page)
prev_button.pack(side=tk.LEFT, padx=10)

next_button = ttk.Button(window, text="下一頁", command=next_page)
next_button.pack(side=tk.RIGHT, padx=10)

window.mainloop()