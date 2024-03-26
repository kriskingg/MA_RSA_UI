import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox

def upload_file():
    filename = filedialog.askopenfilename()
    file_path_entry.delete(0, 'end')
    file_path_entry.insert(0, filename)

def calculate_rsi(data, column='Price', period=14):
    delta = data[column].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    RS = gain / loss
    RSI = 100 - (100 / (1 + RS))
    return RSI

def calculate_drawdowns(data, column='Price'):
    cumulative_max = data[column].cummax()
    drawdown = (data[column] - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min()
    average_drawdown = drawdown.mean()
    return max_drawdown, average_drawdown

def calculate_pullback_time(data, column='Price'):
    cumulative_max = data[column].cummax()
    drawdown = (data[column] - cumulative_max) < 0
    pullback_time = drawdown.cumsum()
    return pullback_time

def generate_plots():
    file_path = file_path_entry.get()
    date_column = date_column_entry.get()
    price_column = price_column_entry.get()

    if not file_path or not date_column or not price_column:
        messagebox.showwarning("Input Error", "Please provide all required inputs.")
        return

    try:
        data = pd.read_excel(file_path)
        data[date_column] = pd.to_datetime(data[date_column])
        data.set_index(date_column, inplace=True)
        data['MA_20'] = data[price_column].rolling(window=20).mean()
        data['MA_50'] = data[price_column].rolling(window=50).mean()
        data['MA_100'] = data[price_column].rolling(window=100).mean()
        data['MA_200'] = data[price_column].rolling(window=200).mean()
        data['RSI'] = calculate_rsi(data, price_column)
        max_drawdown, average_drawdown = calculate_drawdowns(data, price_column)

        plt.figure(figsize=(12, 8))
        plt.subplot(2, 1, 1)
        plt.plot(data.index, data[price_column], label='Price', color='black', linewidth=2)
        plt.plot(data.index, data['MA_20'], label='MA 20', color='blue')
        plt.plot(data.index, data['MA_50'], label='MA 50', color='red')
        plt.plot(data.index, data['MA_100'], label='MA 100', color='green')
        plt.plot(data.index, data['MA_200'], label='MA 200', color='orange')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Price and Moving Averages')
        plt.legend()
        plt.grid(True)

        plt.subplot(2, 1, 2)
        plt.plot(data.index, data['RSI'], label='RSI', color='purple')
        plt.axhline(70, linestyle='--', color='red')
        plt.axhline(30, linestyle='--', color='green')
        plt.xlabel('Date')
        plt.ylabel('RSI')
        plt.title('Relative Strength Index')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

        messagebox.showinfo("Drawdown Info", f"Max Drawdown: {max_drawdown*100:.2f}%\nAverage Drawdown: {average_drawdown*100:.2f}%")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

root = Tk()
root.title("Data Plotter GUI")

Label(root, text="File Path:").grid(row=0, column=0, sticky='w')
file_path_entry = Entry(root, width=50)
file_path_entry.grid(row=0, column=1)
Button(root, text="Upload", command=upload_file).grid(row=0, column=2)

Label(root, text="Date Column Name:").grid(row=1, column=0, sticky='w')
date_column_entry = Entry(root, width=50)
date_column_entry.grid(row=1, column=1, columnspan=2)

Label(root, text="Price Column Name:").grid(row=2, column=0, sticky='w')
price_column_entry = Entry(root, width=50)
price_column_entry.grid(row=2, column=1, columnspan=2)

Button(root, text="Generate Plots", command=generate_plots).grid(row=3, column=0, columnspan=3)

root.mainloop()
