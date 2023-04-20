import tkinter as tk
from tkinter import ttk
import googlemaps
import webbrowser
from search import search_places

# Google Maps API Key
API_KEY = 'AIzaSyCJxyreN2bQmxOgYTLL-BqcAVXNnA714jY'

display_count = 10

# Create Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

# Global variables
results = []
current_page = 0
total_pages = 0

def search():
    global results, current_page, total_pages
    
    # Clear previous search results
    tree.delete(*tree.get_children())
    pages_label.configure(text="")
    map_label.configure(text="圖片參考")
    
    # Get search area and rating from user inputs
    area = entry.get().strip()
    rating = None
    if rating_combobox.get() != "不限評分":
        rating = float(rating_combobox.get())
    
    # Call search_places function from search.py to search for restaurants
    results = search_places(area, rating)
    total_pages = (len(results) - 1) // 10 + 1
    current_page = 0
    
    # Show search results on the treeview
    show_results()

def show_results():
    global current_page
    
    # Calculate start and end index for current page
    start_index = current_page * 10
    end_index = start_index + 10
    
    # Show current page number and total pages
    pages_label.configure(text=f"第{current_page + 1}頁，共{total_pages}頁")
    
    # Show search results on the treeview
    for result in results[start_index:end_index]:
        tree.insert("", "end", values=(result['name'], result['address'], result.get('rating', "-")))
    
def prev_page():
    global current_page
    
    # Do nothing if already on first page
    if current_page == 0:
        return
    
    # Move to previous page and show results
    current_page -= 1
    show_results()

def next_page():
    global current_page
    
    # Do nothing if already on last page
    if current_page == total_pages - 1:
        return
    
    # Move to next page and show results
    current_page += 1
    show_results()

def show_map(location):
    if location == "":
        return
    
    # Show map on Google Maps website
    url = f"https://www.google.com/maps/search/?api=1&query={location}"
    webbrowser.open_new_tab(url)

# Create main window
window = tk.Tk()
window.geometry("1000x800")
window.title("餐廳搜尋系統")

# Create and configure styles for widgets
style = ttk.Style(window)
style.theme_use("clam")
style.configure(".", font=("Helvetica", 12))
style.configure("TLabel", foreground="black", background="white")
style.configure("TButton", foreground="white", background="#0078d7")
style.map("TButton", background=[("active", "#0065a0")])
search_label = ttk.Label(window, text="請輸入地區：")
search_label.pack(pady=(30, 10))
entry = ttk.Entry(window, width=40)
entry.pack()
entry.focus()

rating_label = ttk.Label(window, text="評分：")
rating_label.pack(pady=(10, 0))
rating_combobox = ttk.Combobox(window, width=10, values=["不限評分", "3.0", "3.5", "4.0", "4.5", "5.0"])
rating_combobox.current(0)
rating_combobox.pack()

search_button = ttk.Button(window, text="搜尋", command=search)
search_button.pack(pady=(20, 10))

pages_label = ttk.Label(window, text="")
pages_label.pack()

tree = ttk.Treeview(window, columns=("name", "address", "rating"), show="headings")
tree.heading("name", text="餐廳名稱")
tree.heading("address", text="地址")
tree.heading("rating", text="評分")
tree.column("name", width=200, anchor="center")
tree.column("address", width=400, anchor="w")
tree.column("rating", width=100, anchor="center")
tree.pack(padx=20, pady=20)

prev_button = ttk.Button(window, text="上一頁", command=prev_page)
prev_button.pack(side="left", padx=(20, 10))

next_button = ttk.Button(window, text="下一頁", command=next_page)
next_button.pack(side="left")

map_label = ttk.Label(window, text="圖片參考")
map_label.pack(pady=(20, 0))

if __name__ == '__main__':
    window.mainloop()