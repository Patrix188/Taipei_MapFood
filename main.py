import tkinter as tk
from tkinter import ttk
from search import search_places
import googlemaps
import requests
from io import BytesIO
from PIL import Image, ImageTk
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

import io
import tkinter as tk
from PIL import ImageTk, Image

def show_map():
    selection = tree.selection()
    if selection:
        item = tree.item(selection[0])
        name = item['values'][0]
        for result in results:
            if result['name'] == name:
                place_id = result['place_id']
                place = gmaps.place(place_id, language='zh-TW', fields=['name', 'formatted_address', 'rating', 'photo'])['result']
                name = place['name']
                address = place['formatted_address']
                rating = place.get('rating', None)
                photo_reference = place.get('photos', [])[0].get('photo_reference', None)
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={API_KEY}" if photo_reference is not None else None
                
                # 產生 Google Maps 的查詢網址
                query = f"https://www.google.com/maps/search/?api=1&query={address}&query_place_id={place_id}"
                webbrowser.open(query)
                
                # 顯示餐廳照片和資訊
                if photo_url is not None:
                    # 讀取照片
                    response = requests.get(photo_url)
                    img = Image.open(io.BytesIO(response.content))
                    
                    # 建立小視窗
                    window = tk.Toplevel()
                    window.title(name)
                    
                    # 顯示照片
                    img_tk = ImageTk.PhotoImage(img)
                    label_photo = tk.Label(window, image=img_tk)
                    label_photo.pack()
                    
                    # 創建工具列
                    toolbar = tk.Frame(window, bg='white', height=40)
                    toolbar.pack(side=tk.TOP, fill=tk.X)
                    back_button = tk.Button(toolbar, text='返回', command=window.destroy)
                    back_button.pack(side=tk.LEFT, padx=5, pady=5)

                    # 顯示餐廳資訊
                    frame_info = tk.Frame(window)
                    frame_info.pack(pady=10)
                    
                    label_name = tk.Label(frame_info, text=name, font=('Arial', 16, 'bold'))
                    label_name.grid(row=0, column=0, columnspan=2, sticky='w')
                    
                    label_address_title = tk.Label(frame_info, text='地址：', font=('Arial', 12))
                    label_address_title.grid(row=1, column=0, sticky='e')
                    label_address_value = tk.Label(frame_info, text=address, font=('Arial', 12))
                    label_address_value.grid(row=1, column=1, sticky='w')
                    
                    label_rating_title = tk.Label(frame_info, text='評分：', font=('Arial', 12))
                    label_rating_title.grid(row=2, column=0, sticky='e')
                    label_rating_value = tk.Label(frame_info, text=rating, font=('Arial', 12))
                    label_rating_value.grid(row=2, column=1, sticky='w')
                    
                    window.mainloop()
                break
    else:
        print("請選擇店家")


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
location_entry.pack(anchor=tk.CENTER, pady=20)

map_button = tk.Button(window, text="打開地圖查看", command=lambda: show_map())
map_button.pack(anchor=tk.CENTER)

prev_button = ttk.Button(window, text="上一頁", command=prev_page)
prev_button.pack(side=tk.LEFT, padx=10)

next_button = ttk.Button(window, text="下一頁", command=next_page)
next_button.pack(side=tk.RIGHT, padx=10)

window.mainloop()