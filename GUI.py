import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import webbrowser
import os

from RSSQL import *
from main import *
from wallet import wllt
from portfolio import prtfl
from exAPI import *


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Rise & Shine')
        self.geometry('1200x800')
        self.configure(bg='grey')
        self.resizable(False, False)
        self.iconbitmap('icon.ico')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - 1200 / 2)
        center_y = int(screen_height / 2 - 800 / 2)
        self.geometry(f'1200x800+{center_x}+{center_y}')

        self.style = ttk.Style(self)
        self.style.configure('start.TButton',font=('Verdana',25))
        self.style.configure('T3.TFrame', background='gray')
        self.style.configure('menu.TButton', font=('Verdana',12))

        # start of GUI
        self.logo=ImageTk.PhotoImage(Image.open('logo.png'))
        self.label_biglogo = ttk.Label(self,image=self.logo, compound='image')
        self.label_biglogo.place(relx=0.5, rely=0.4, anchor='n')
        self.button_start = ttk.Button(self,text='START', style='start.TButton',command=lambda: self.start_button(self))
        self.button_start.place(relx=0.5, rely=0.6, anchor='n')

        # end frame
        self.endframe=ttk.Frame (self, height=800, width=1200)
        self.label_thankyou=ttk.Label(self.endframe,text='Thank you for using', font=('Verdana',25))
        self.label_thankyou.place(relx=0.5, rely=0.3, anchor='n')
        self.label_biglogo2 = ttk.Label(self,image=self.logo, compound='image')
        self.label_biglogo2.place(relx=0.5, rely=0.4, anchor='n')
        self.button_close=ttk.Button(self.endframe,text='Close', style='menu.TButton', command=lambda: self.close(self))
        self.button_close.place(relx=0.5, rely=0.7, anchor='n')

        # app frames
        self.lframe=ttk.Frame (self, height=800, width=215, padding= (5,10,5,10))
        self.rframe=ttk.Frame(self, height=80, width=985, padding= (5,10,5,10))
        self.mainframe=ttk.Frame(self, height=720, width=985, style='T3.TFrame', padding= (5,10,5,10))
        self.idframe=ttk.Frame(self.mainframe,height=700, width=50, padding= (5,10,5,10))

        # idframe - lable and portfolio id selection
        self.label_id=ttk.Label(self.idframe, text='Portfolio ID:', font=('Verdana', 12), padding=(0,0,0,10))
        self.combo_portfid = ttk.Combobox(self.idframe, width=14)
        self.label_id.pack()
        self.combo_portfid.pack()

        # right top frame - Wallet
        self.label_wallet=ttk.Label(self.rframe,padding=(5,10,5,10), font=('Verdana', 17))
        self.label_wallet.place(relx=1, rely=0, anchor='ne')

        # left frame - Menu
        self.smallogo = ImageTk.PhotoImage(Image.open('logo.png').resize((200, 75)))
        self.label_smalllogo=ttk.Label(self.lframe, image=self.smallogo, compound='image')
        self.label_smalllogo.place(x=0,y=0, anchor='nw')
        self.label_menu=ttk.Label(self.lframe, text='MENU', font=('Verdana',25))
        self.label_menu.place(relx=0.5,rely=0.15,anchor='n')
        self.button_portfolios=ttk.Button(self.lframe,text='Portfolios', style='menu.TButton', command=lambda: self.portfolios_view(self))
        self.button_portfolios.place(relx=0.5,rely=0.25,anchor='n')
        self.button_portf_overview=ttk.Button(self.lframe,text='Portfolio overview', style='menu.TButton', command=lambda: self.portf_overview(self))
        self.button_portf_overview.place(relx=0.5,rely=0.30,anchor='n')
        self.button_portf_performance=ttk.Button(self.lframe,text='Portfolio performance', style='menu.TButton', command=lambda: self.portf_performance(self))
        self.button_portf_performance.place(relx=0.5,rely=0.35,anchor='n')
        self.button_search=ttk.Button(self.lframe,text='Search for ticker', style='menu.TButton', command=lambda: self.search(self))
        self.button_search.place(relx=0.5,rely=0.40,anchor='n')
        self.button_ticker_info=ttk.Button(self.lframe,text='Ticker performance', style='menu.TButton', command=lambda: self.ticker_info(self))
        self.button_ticker_info.place(relx=0.5,rely=0.45,anchor='n')
        self.button_buysell=ttk.Button(self.lframe,text='Buy / Sell', style='menu.TButton', command=lambda: self.buy_sell(self))
        self.button_buysell.place(relx=0.5,rely=0.50,anchor='n')
        self.button_close=ttk.Button(self.lframe,text='Start/Close portfolio', style='menu.TButton', command=lambda: self.start_close_portf(self))
        self.button_close.place(relx=0.5,rely=0.55,anchor='n')
        self.button_wallet=ttk.Button(self.lframe,text='Wallet', style='menu.TButton', command=lambda:self.wallet_change(self))
        self.button_wallet.place(relx=0.5,rely=0.60,anchor='n')
        self.button_API = ttk.Button(self.lframe, text='API', style='menu.TButton',command=lambda: self.API_start(self))
        self.button_API.place(relx=0.5, rely=0.9, anchor='n')

        # main frame (will be config by functions below)
        self.scrolledtext_data = scrolledtext.ScrolledText(self.mainframe)
        self.button_graph = ttk.Button(self.mainframe)
        self.text = tk.StringVar()
        self.number=tk.StringVar()
        self.textbox = ttk.Entry(self.mainframe, textvariable=self.text, width=45, font=('Verdana', 12))
        self.numberbox=ttk.Entry(self.mainframe, textvariable=self.number, width=45, font=('Verdana', 12))
        self.button_buy = ttk.Button(self.mainframe, style='menu.TButton')
        self.button_sell = ttk.Button(self.mainframe, style='menu.TButton')
        self.button_show = ttk.Button(self.mainframe, text='Show', style='menu.TButton' )
        self.graph_image = None

    def start_button(self,window):
        global con, mycursor, portfolios_dict, tickers, mywallet
        mywallet = wllt()
        tickers = pd.DataFrame()
        con, mycursor = DBconnection(config(), True) # TO BE CHANGE TO TRUE !!!
        portfolios_dict = fetch_portfolios(mycursor)
        load_portfolios(portfolios_dict, mycursor)
        mywallet.curvalue = mywallet.CurrentValue(mycursor)
        self.label_wallet.config(text='Wallet: $' + str(mywallet.curvalue))
        self.label_biglogo.destroy()
        self.button_start.destroy()
        self.lframe.place(relx=0,rely=0, anchor='nw')
        self.rframe.place(x=1200,y=0,anchor='ne')
        self.mainframe.place(x=1200,y=80,anchor='ne')
        self.combo_portfid.configure(values=list(portfolios_dict.keys()))
        self.combo_portfid.set('Pick portfolio ID')

    def portfolios_view(self,window):
        global portfolios_dict
        self.clear_mainframe()
        self.scrolledtext_data.insert(tk.INSERT, 'ID - NAME - CURRENT $ VALUE')
        self.data_to_scrolledtext(portfolios_overview(portfolios_dict),'list')
        self.scrolledtext_data.configure(height=44, width=90)
        self.scrolledtext_data.place(relx=0, rely=0, anchor='nw')

    def portf_overview(self,window):
        self.clear_mainframe()
        self.idframe.place(relx=1, rely=0, anchor='ne')
        self.button_show.configure(command=lambda: self.show('portf_overview'))
        self.button_show.place(relx=1, rely=0.15, anchor='ne')

    def portf_performance(self,window):
        self.clear_mainframe()
        self.idframe.place(relx=1, rely=0, anchor='ne')
        self.button_show.configure(command=lambda: self.show('portf_performance'))
        self.button_show.place(relx=1, rely=0.15, anchor='ne')

    def search(self,window):
        self.clear_mainframe()
        global tickers
        if tickers.size==0: tickers=API_get_tickers()
        self.textbox.insert(tk.END, 'What are you searching for?')
        self.textbox.place(relx=0, rely=0.0, anchor='nw')
        self.button_show.configure(command=lambda: self.show('search'))
        self.button_show.place(relx=0.55, rely=0.0, anchor='nw')

    def ticker_info(self,window):
        self.clear_mainframe()
        self.textbox.insert(tk.END, 'Insert required ticker')
        self.numberbox.insert(tk.END, 'Insert required interval: 1, 5, 15, 30, 60 (minutes)')
        self.textbox.place(relx=0, rely=0.0, anchor='nw')
        self.numberbox.place(relx=0, rely=0.05, anchor='nw')
        self.button_show.configure(command=lambda: self.show('ticker_info'))
        self.button_show.place(relx=0.55, rely=0.0, anchor='nw')

    def buy_sell(self,window):
        self.clear_mainframe()
        self.idframe.configure(height=30)
        self.idframe.place(relx=0, rely=0, anchor='nw')
        self.textbox.insert(tk.END, 'Insert required ticker')
        self.numberbox.insert(tk.END, 'Insert required volume')
        self.textbox.place(relx=0, rely=0.15, anchor='nw')
        self.numberbox.place(relx=0, rely=0.25, anchor='nw')
        self.button_buy.configure(text='Buy', command=lambda: self.buy_sell_fc('buy'))
        self.button_sell.configure(text='Sell', command=lambda: self.buy_sell_fc('sell'))
        self.button_buy.place(relx=0, rely=0.35, anchor='nw')
        self.button_sell.place(relx=0.15, rely=0.35, anchor='nw')

    def buy_sell_fc(self, command):
        global portfolios_dict, mycursor, mywallet
        id = self.get_portf_id()
        if id is None: return
        ticker=self.textbox.get()
        volume=self.numberbox.get()
        try: volume=int(volume)
        except:
            messagebox.showinfo("Warning", "Volume must be whole number")
            return
        if command=='buy':
            try: message=portfolios_dict[id].buy(mycursor, mywallet, ticker, volume)
            except:
                messagebox.showinfo("Warning", "Incorrect ticker input. Please search for correct ticker in menu.")
                return
        elif command=='sell': message=portfolios_dict[id].sell(mycursor, mywallet, ticker, volume)
        messagebox.showinfo("Info", message)
        portfolios_dict[id].load_hold(mycursor)
        portfolios_dict[id].load_currentvalue(mycursor)
        mywallet.CurrentValue(mycursor)
        self.label_wallet.config(text='Wallet: $' + str(mywallet.curvalue))

    def start_close_portf(self,window):
        self.clear_mainframe()
        self.idframe.configure(height=30)
        self.idframe.place(relx=0.75, rely=0.1, anchor='n')
        self.textbox.insert(tk.END, 'Insert required name of the new portfolio')
        self.textbox.place(relx=0.25, rely=0.15, anchor='n')
        self.button_buy.configure(text='Start', command=lambda: self.start_close_portf_fc('start'))
        self.button_sell.configure(text='Close', command=lambda: self.start_close_portf_fc('close'))
        self.button_buy.place(relx=0.25, rely=0.25, anchor='n')
        self.button_sell.place(relx=0.75, rely=0.25, anchor='n')

    def start_close_portf_fc(self,command):
        global portfolios_dict, mycursor, mywallet
        if command=='close':
            id = self.get_portf_id()
            if id is None: return
            message=portfolios_dict[id].close(mycursor, mywallet)
            mywallet.CurrentValue(mycursor)
            self.label_wallet.config(text='Wallet: $' + str(mywallet.curvalue))
        elif command=='start':
            name=self.textbox.get()
            if name=='Insert required name of the new portfolio':
                messagebox.showinfo("Warning",'Please insert required name of the new portfolio')
                return
            message=start_portfolio(name, portfolios_dict, mycursor)
            self.combo_portfid.configure(values=list(portfolios_dict.keys()))
        messagebox.showinfo("Info", message)

    def wallet_change(self,window):
        global mycursor
        self.clear_mainframe()
        self.numberbox.insert(tk.END, 'Insert required amount')
        self.numberbox.place(relx=0, rely=0.0, anchor='nw')
        self.button_buy.configure(text='Deposit', command=lambda: self.money('deposit'))
        self.button_sell.configure(text='Withdraw', command=lambda: self.money('withdraw'))
        self.button_buy.place(relx=0, rely=0.05, anchor='nw')
        self.button_sell.place(relx=0.15, rely=0.05, anchor='nw')
        self.data_to_scrolledtext(mywallet.ShowRecords(mycursor), 'df')
        self.scrolledtext_data.configure(height=30, width=90)
        self.scrolledtext_data.place(relx=0, rely=0.2, anchor='nw')

    def money(self,operation):
        global mywallet, mycursor
        amount=self.numberbox.get()
        try: amount=float(amount)
        except:
            messagebox.showinfo("Warning", "Amount need to be float number in format ***.**")
            return
        if operation=='deposit':
            mywallet.WriteRecord(mycursor,amount,'User deposit')
        elif operation=='withdraw':
            if amount>mywallet.curvalue:
                messagebox.showinfo("Warning", "There is not enough money in the wallet")
                return
            mywallet.WriteRecord(mycursor, -amount, 'User withdrawal')
        mywallet.CurrentValue(mycursor)
        self.label_wallet.config(text='Wallet: $' + str(mywallet.curvalue))
        self.scrolledtext_data.delete(1.0, tk.END)
        self.data_to_scrolledtext(mywallet.ShowRecords(mycursor), 'df')

    def API_start(self,window):
        self.clear_mainframe()
        answer = messagebox.askokcancel("Start API", "This will close GUI and start API. You need to run the API file. Correct webpage will be opened for you. Do you want to continue?")
        if answer:
            try:
                os.system("start "+"API.py")
            except:
                messagebox.showinfo("Start API", "Please open and run the API file located in the project folder.")
            finally:
                webbrowser.open('http://127.0.0.1:5000', new=0, autoraise=False)
                self.destroy()

    def close(self,window):
        self.destroy()

    def on_closing(self):
        global con, mycursor
        DBend(con, mycursor)
        self.mainframe.destroy()
        self.rframe.destroy()
        self.lframe.destroy()
        self.endframe.place(x=0, y=0, anchor='nw')

    def clear_mainframe(self):
        self.scrolledtext_data.delete(1.0, tk.END)
        self.textbox.delete(0, tk.END)
        self.numberbox.delete(0, tk.END)
        for widget in self.mainframe.winfo_children():
            widget.place_forget()

    def get_portf_id(self):
        id = self.combo_portfid.get()
        if id == 'Pick portfolio ID':
            messagebox.showinfo("Warning", "You need to choose portfolio.")
            return
        return int(id)

    def data_to_scrolledtext(self,array,method):
        if method=='df':
            self.scrolledtext_data.insert(tk.INSERT, array.to_string(max_rows=None, justify='center', index=False))
            return self
        elif method=='np':
            data=array.tolist()
        elif method=='list':
            data=array
        for record in data:
            self.scrolledtext_data.insert(tk.INSERT, '\n')
            self.scrolledtext_data.insert(tk.INSERT, record)
        return self

    def on_click(self,graph_obj):
        graph_obj.show()

    def show(self, command):
        global portfolios_dict, mycursor, tickers
        if command=='portf_overview':
            id = self.get_portf_id()
            if id is None: return
            self.scrolledtext_data.insert(tk.INSERT, 'ID: ' +str(id)+ '\n')
            self.scrolledtext_data.insert(tk.INSERT, 'NAME: '+portfolios_dict[id].name+'\n')
            self.scrolledtext_data.insert(tk.INSERT, 'CURRENT VALUE: '+str(portfolios_dict[id].current_value)+'\n')
            self.scrolledtext_data.insert(tk.INSERT, 'HOLD: (ticker - volume held - current stock price)')
            self.data_to_scrolledtext(portfolios_dict[id].hold,'np')
            self.scrolledtext_data.configure(height=44, width=90)
            self.scrolledtext_data.place(relx=0, rely=0, anchor='nw')
            self.scrolledtext_data.insert(tk.INSERT,'\n\n')
        elif command=='portf_performance':
            self.scrolledtext_data.delete(1.0, tk.END)
            id = self.get_portf_id()
            if id is None: return
            self.scrolledtext_data.insert(tk.INSERT,'DATE - VALUE - % CHANGE')
            self.data_to_scrolledtext(portfolios_dict[id].historic_value,'np')
            self.scrolledtext_data.configure(height=44, width=30)
            self.scrolledtext_data.place(relx=0, rely=0, anchor='nw')
            graph, path=portfolios_dict[id].graph_performance(mycursor)
            self.graph_image=ImageTk.PhotoImage(Image.open(path).resize((665, 475)))
            self.button_graph.configure(image=self.graph_image, command=lambda :self.on_click(graph))
            self.button_graph.place(relx=0.3, rely=0.25, width=665, height=475, anchor='nw')
        elif command=='ticker_info':
            self.scrolledtext_data.delete(1.0, tk.END)
            ticker = self.textbox.get()
            interval = self.numberbox.get()
            try: interval=int(interval)
            except:
                messagebox.showinfo("Warning", "Interval must have value 1, 5, 15, 30 or 60")
                return
            if interval not in [1, 5, 15, 30, 60]:
                messagebox.showinfo("Warning", "Interval must have value 1, 5, 15, 30 or 60")
                return
            intraday_data=API_intraday(ticker,interval)
            if intraday_data.size==2:
                messagebox.showinfo("Warning", "Incorrect ticker input. Please search for correct ticker in menu.")
                return
            self.data_to_scrolledtext(intraday_data,'df')
            self.scrolledtext_data.configure(height=11, width=80)
            self.scrolledtext_data.place(relx=0, rely=0.1, anchor='nw')
            graph, path=API_get_ticker_graph(intraday_data,ticker)
            self.graph_image=ImageTk.PhotoImage(Image.open(path).resize((650, 450)))
            self.button_graph.configure(image=self.graph_image, command=lambda :self.on_click(graph))
            self.button_graph.place(relx=0, rely=0.37, width=650, height=450, anchor='nw')
        elif command=='search':
            text=self.textbox.get()
            if text=='What are you searching for?':
                messagebox.showinfo("Missing", "Input required text for search")
                return
            self.data_to_scrolledtext(API_search_ticker(tickers,text), 'df')
            self.scrolledtext_data.configure(height=44, width=80)
            self.scrolledtext_data.place(relx=0, rely=0.05, anchor='nw')
            self.scrolledtext_data.insert(tk.INSERT, '\n\n')


if __name__ == "__main__":
    gui = GUI()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        gui.mainloop()
