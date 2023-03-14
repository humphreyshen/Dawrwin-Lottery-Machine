#%%
from tkinter import * 
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pickle
from PIL import Image, ImageTk
import traceback #可提供詳細bug位置
import requests
import json
import pymysql
import pandas as pd
import os
#%%

class Interface:
    """Create GUI interface for classfication program"""

    def __init__(self):
        self.window = Tk() #建立屬性(變數)：self.window = Tk()
        Tk.report_callback_exception = self.report_callback_exception  # Exception Handling by using traceback module
        self.window.title("Data_Resort Lottery Machine") #Tk().title
        self.window.resizable(False, False) #Tk().resizable()
        #self.window.wm_iconbitmap("./docs/Data_Resort_icon.ico") #Tk().wm_iconbitmap()
        self.canvas = Canvas(self.window, width=450, height=300) #建立屬性(變數)：self.canvas = Canvas()
        self.canvas.pack() #Canvas().pack()
        self.mes_path = ""
        self.context_font = ("微軟正黑體", 10) #建立屬性(變數)
        self.button_font = ("微軟正黑體", 9, "underline") #self.button_font (object-orientation) #建立屬性(變數)
        self.title_font = ("微軟正黑體", 15, "bold") #建立屬性(變數)
        
    def report_callback_exception(self, *args):
        """Catch errors"""
        err = traceback.format_exception(*args)
        messagebox.showerror("Exception", err)

    def new_window(self, title, geo, unclosable=False):
        """Create a new window."""
        newW = Toplevel(self.window)
        newW.title(title)
        newW.geometry(geo)
        newW.resizable(False, False)
        #newW.wm_iconbitmap("./docs/pic/" + icon)
        newW.grab_set()
        if unclosable:
            newW.protocol("WM_DELETE_WINDOW", self.on_closing)  # unclosable
        return newW

    def on_closing(self):
        """Make it unclosable"""
        pass

    def lobby(self):
        # welcome image
        img = Image.open('./docs/Data_Resort_Logo_black_word.png')
        resized_image=img.resize((350,350))
        tk_img = ImageTk.PhotoImage(resized_image)
        canvas = Canvas(self.window, width=300, height=120)
        canvas.create_image(150, 60, anchor='center', image=tk_img)
        canvas.place(x=80, y= 20)


        # user information
        Label(self.window, text='User name: ').place(x=50, y= 150)
        Label(self.window, text='Password: ').place(x=50, y= 190)
        Label(self.window, text='(The Program is created by Humphrey Shen)').place(x=80, y= 270)

        self.var_usr_name = tk.StringVar()
        self.var_usr_pwd = tk.StringVar()
        entry_usr_name = tk.Entry(self.window, textvariable=self.var_usr_name)
        entry_usr_name.place(x=160, y=150)
        self.entry_usr_pwd = tk.Entry(self.window, textvariable=self.var_usr_pwd, show='*')
        self.entry_usr_pwd.place(x=160, y=190)
        
        # Quit button
        quit_but = Button( 
            self.window,
            text="Quit",
            font=self.button_font,
            relief="groove", # button 3D style
            command=self.window.destroy, #destroy
        )
        quit_but.place(x=300, y=230)
        
        btn_login = Button( 
            self.window,
            text="Login",
            font=self.button_font,
            relief="groove", # button 3D style
            command=self.usr_login, 
        )
        btn_login.place(x=100, y=230)
        
        
        btn_sign_up = Button( 
            self.window,
            text="Sign up",
            font=self.button_font,
            relief="groove", # button 3D style
            command=self.usr_sign_up, 
        )
        btn_sign_up.place(x=190, y=230)
        self.window.mainloop()
        
    
    def usr_login(self):
        usr_name = self.var_usr_name.get()
        usr_pwd = self.var_usr_pwd.get()
        try:
            with open('usrs_info.pickle', 'rb') as usr_file:
                usrs_info = pickle.load(usr_file)
        except FileNotFoundError:
            with open('usrs_info.pickle', 'wb') as usr_file:
                usrs_info = {'admin': 'admin'}
                pickle.dump(usrs_info, usr_file)

        if usr_name in usrs_info:

            if usr_pwd == usrs_info[usr_name]:
                tk.messagebox.showinfo(title='Welcome', message= usr_name + ', How are you? ' + '\nWelcome to the program')
                self.login_page=self.new_window("Data_Resort Lottery Machine", "450x300")
                self.login_page.wm_iconbitmap("./docs/Data_Resort_icon.ico")
                Label(self.login_page, text='・本程式所屬權為：Data_Resort').place(x=50, y= 80)
                Label(self.login_page, text='・如您欲授權更改，請與作者聯繫').place(x=50, y= 100)
                Label(self.login_page, text='・本版本為：Darwin Beta 1.0').place(x=50, y= 120)
                Label(self.login_page, text='・如您同意上述，請點選下方按鈕進入主程式').place(x=50, y= 140)
                enter_but = Button(
                    self.login_page,
                    text="進入主程式",
                    font=self.button_font,
                    relief="groove", # button 3D style
                    command=self.main_page, #enter_main_page
                )
                enter_but.place(x=180, y=180) #The position of the button

            else:
                tk.messagebox.showerror(message='Error, your password is wrong, try again.')
        else:
            is_sign_up = tk.messagebox.askyesno('Welcome',
                                'You have not sign up yet. Sign up today?')
            if is_sign_up:
                self.usr_sign_up()

    def usr_sign_up(self):
        def sign_to_lottery():
            np = new_pwd.get()
            npf = new_pwd_confirm.get()
            nn = new_name.get()
            with open('usrs_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
            if np != npf:
                tk.messagebox.showerror('Error', 'Password and confirm password must be the same!')
            elif nn in exist_usr_info:
                tk.messagebox.showerror('Error', 'The user has already signed up!')
            else:
                exist_usr_info[nn] = np
                with open('usrs_info.pickle', 'wb') as usr_file:
                    pickle.dump(exist_usr_info, usr_file)
                tk.messagebox.showinfo('Welcome', 'You have successfully signed up!')
                window_sign_up.destroy()
        window_sign_up = tk.Toplevel(self.window )
        window_sign_up.geometry('350x200')
        window_sign_up.title('Sign up window')

        new_name = tk.StringVar()
        tk.Label(window_sign_up, text='User name: ').place(x=10, y= 10)
        entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
        entry_new_name.place(x=150, y=10)

        new_pwd = tk.StringVar()
        tk.Label(window_sign_up, text='Password: ').place(x=10, y=50)
        entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
        entry_usr_pwd.place(x=150, y=50)

        new_pwd_confirm = tk.StringVar()
        tk.Label(window_sign_up, text='Confirm password: ').place(x=10, y= 90)
        entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
        entry_usr_pwd_confirm.place(x=150, y=90)

        btn_comfirm_sign_up = tk.Button(window_sign_up, text='Sign up', command=sign_to_lottery)
        btn_comfirm_sign_up.place(x=150, y=130)
    
    def get_dir(self, entry):
            """Ask the user for a directory."""
            self.mes_path = filedialog.askdirectory(title="Select folder")
            if entry.get() == "":
                entry.insert(0, self.mes_path)
            else:
                entry.delete(0, "end")
                entry.insert(0, self.mes_path)
                

        
    def main_page(self):
        self.login=self.new_window("Data_Resort Lottery Machine", "450x300")
        self.login.wm_iconbitmap("./docs/Data_Resort_icon.ico")
        Label(self.login, text="Please select your directory of your ouput file.", justify='left').place(x=50, y=10)
        Label(self.login, text='Ouptut File Name:').place(x=50, y= 80)
        Label(self.login, text='Please Enter Your Token:').place(x=50, y= 120)
        Label(self.login, text='Please Enter Your PostID:').place(x=50, y= 160)
        Label(self.login, text='Please Enter Your Price:').place(x=50, y= 200)
        Label(self.login, text='Count:').place(x=325, y= 200)
        self.dir_entry = Entry(self.login, width=20)
        self.ouput_name=tk.StringVar()        
        self.token = tk.StringVar()
        self.PostID = tk.StringVar()
        self.Price = tk.StringVar()
        self.var=tk.StringVar()
        self.var.set('1')
        ouput_name=tk.Entry(self.login, textvariable=self.ouput_name)
        entry_token = tk.Entry(self.login , textvariable=self.token)
        entry_PostID = tk.Entry(self.login , textvariable=self.PostID)
        entry_Price = tk.Entry(self.login , textvariable=self.Price, width=10)
        myoptionmenu = tk.OptionMenu(self.login, self.var, '2','3','4','5','6','7','8','9','10')
        dir_but = Button(
            self.login,
            text="Ouput Directory",
            font=("微軟正黑體", 8),
            command=lambda: self.get_dir(self.dir_entry), #lambda
        )
        dir_but.place(x=50, y=40)
        self.dir_entry.place(x=220, y=40)
        ouput_name.place(x=220, y=80)
        entry_token.place(x=220, y=120)
        entry_PostID.place(x=220, y=160)
        entry_Price.place(x=220, y=200)
        myoptionmenu.place(x=370 ,y=200)
        
        def do_lottery(): 
                try: 
                    ouputName=self.ouput_name.get()
                    postID=self.PostID.get()
                    token=self.token.get()
                    path=self.dir_entry.get()
                    price_count=self.var.get()
                    price_name=self.Price.get()
                    url = 'https://graph.facebook.com/v15.0/'+postID+'/comments?access_token='+token
                    response = requests.get(url)
                    text = json.loads(response.text) 
                    user_name = text['data'][0]['from']['name']
                    user_id = text['data'][0]['from']['id']
                    message = text['data'][0]['message']
                    PostID = text['data'][0]['id'] 
                    #Put data into dataframe
                    data={
                        'PrcieName':[price_name],
                        'PostID':[PostID],
                        'UserID':[user_id],
                        'UserName':[user_name],
                        'Message':[message]
                        }
                    df=pd.DataFrame(data=data)
                    random_choice=df.sample(int(price_count))
                    # to csv file
                    os.makedirs(path, exist_ok=True)
                    random_choice.to_csv('{}/{}.csv'.format(path,ouputName), encoding='utf-8-sig')
                    tk.messagebox.showinfo(title='Sucess', message='Lottery has Run Succesfully')
                except:
                    tk.messagebox.showinfo(title='Fail', message='You May Missing Some Arguments.\rPlease Check Again.')
                
        #ask for activate
        btn_activate = Button( 
        self.login,
        text="Activate",
        font=self.button_font,
        relief="groove", # button 3D style
        command=do_lottery
        )
        btn_activate.place(x=200, y=240)
        
        
        
if __name__ == "__main__":
    itf = Interface()
    itf.lobby()



# %%
