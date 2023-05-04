import tkinter as tk
from tkinter import ttk
from search import search_places
import googlemaps
import webbrowser
import folium

API_KEY = 'AIzaSyCJxyreN2bQmxOgYTLL-BqcAVXNnA714jY'
gmaps = googlemaps.Client(key=API_KEY)

# 每頁呈現的結果數量
display_count:int = 5
popup_menu = None


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

def show_map(places):
    # 取得地圖中心點
    lat_sum = 0
    lng_sum = 0
    for place in places:
        lat_sum += place["lat"]
        lng_sum += place["lng"]
    center_lat = lat_sum / len(places)
    center_lng = lng_sum / len(places)

    # 建立地圖
    m = folium.Map(location=[center_lat, center_lng], zoom_start=15)

    # 在地圖上標註每個地點
    for i, place in enumerate(places):
        # 取得店家資訊
        name = place["name"]
        address = place["address"]
        rating = place["rating"]
        url = place["url"]

        # 取得店家位置
        lat = place["lat"]
        lng = place["lng"]

        # 建立標註
        tooltip = f"{i+1}. {name}"
        popup_html = f"""
            <strong>{name}</strong><br>
            {address}<br>
            Rating: {rating}<br>
            <a href="{url}" target="_blank">More info</a>
        """
        popup = folium.Popup(html=popup_html, max_width=500)
        folium.Marker(location=[lat, lng], tooltip=tooltip, popup=popup).add_to(m)

    # 顯示地圖
    m.save("map.html")
    webbrowser.open("map.html")


def open_result_info(event):
    selection = tree.selection()
    if selection:
        item = tree.item(selection[0])
        name = item['values'][0]
        for i, result in enumerate(results):
            if result['name'] == name:
                place_id = result['place_id']
                tree.selection_set(selection[0])
                popup_menu.tk_popup(event.x_root, event.y_root)
                # 取得店家詳細資訊
                place_detail = gmaps.place(place_id)['result']
                # 在控制台上顯示詳細資訊
                print(place_detail)
                break


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

# 創建主視窗
window = tk.Tk()
window.title("地圖搜尋")
window.geometry("800x600")

#創建標籤框架
search_frame = ttk.LabelFrame(window, text="搜尋區域")
search_frame.pack(fill="both", expand="yes", padx=20, pady=20)

#創建搜尋輸入框
entry = ttk.Entry(search_frame, width=30)
entry.pack(side="left", padx=5, pady=5)

#創建搜尋按鈕
search_button = ttk.Button(search_frame, text="搜尋", command=search)
search_button.pack(side="left", padx=5, pady=5)

#創建結果框架
results_frame = ttk.Frame(window)
results_frame.pack(fill="both", expand="yes", padx=20, pady=20)

#創建標題列
columns = ("名稱", "地址", "評分")
tree = ttk.Treeview(results_frame, show="headings", columns=columns)
for col in columns:
    tree.column(col, width=200)
    tree.heading(col, text=col)
    tree.pack(side="left", fill="y")

#創建捲軸條
scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

#創建分頁按鈕
paging_frame = ttk.Frame(window)
paging_frame.pack(pady=20)
prev_button = ttk.Button(paging_frame, text="<< 上一頁", command=prev_page)
prev_button.pack(side="left", padx=5)
next_button = ttk.Button(paging_frame, text="下一頁 >>", command=next_page)
next_button.pack(side="left", padx=5)
pages_label = ttk.Label(paging_frame, text="")
pages_label.pack(side="left", padx=5)

#創建彈出選單
popup_menu = tk.Menu(tree, tearoff=0)
popup_menu.add_command(label="開啟地圖", command=lambda: show_map(entry.get()))

#綁定右鍵事件
tree.bind("<Button-3>", open_result_info)

#執行主迴圈
window.mainloop()
