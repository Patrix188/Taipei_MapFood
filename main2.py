import webbrowser
import tkinter as tk

def open_result_info(results, text):
    selection = text.tag_ranges(tk.SEL)
    if selection:
        index1 = text.index(tk.SEL_FIRST)
        index2 = text.index(tk.SEL_LAST)
        name = text.get(index1, index2).split("\n")[0]
        for result in results:
            if result['name'] == name:
                place_id = result['place_id']
                url = (f"https://www.google.com.tw/maps/place/?q=place_id:{place_id}")
                webbrowser.open(url)

# 測試程式碼
results = [
    {'name': '大安森林公園', 'place_id': 'ChIJVbG6CvUOaDQR6FXHb7VQ2dQ'},
    {'name': '台北101', 'place_id': 'ChIJvyyVr20sQjQRVpBzLzfBvHg'},
    {'name': '國立故宮博物院', 'place_id': 'ChIJtRYEi1cNbzQRT8jKkGB0LxI'}
]

root = tk.Tk()
text = tk.Text(root)
text.insert(tk.END, "大安森林公園\n台北101\n國立故宮博物院")
text.pack()
root.bind("<ButtonRelease-1>", lambda event: open_result_info(results, text))
root.mainloop()