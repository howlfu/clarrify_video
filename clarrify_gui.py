'''
Created on 2017年4月6日

@author: HL
'''
#coding=utf-8
from tkinter import *
from PIL import ImageTk, Image
from Get_dir_info import dir_files
import os
import operator
from pip.utils.hashes import FAVORITE_HASH
from asyncio.tasks import sleep
from macpath import split

class DemoGUI(Frame):
    select_1= 0
    select_2= 0
    select_3= 0
    files_get = object
    search_path = ""
    path_photo = {}
    list_actor_name = {}
    list_works_name = {}
    list_favor_name = {}
    current_select_act =""
    current_select_work= ""
    current_select_favor=""
    faverit = {}
    movie_path = ""
    favor_file = "favor.txt"
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.search_path = 'D:\GitHub\movies'
        self.files_get = dir_files()
        self.grid()
        self["background"] = "gray"
        self.createWidgets()
        
    def createWidgets(self):
        #index
        #self.Text_for_save1 = Label(self, text = u"預覽圖", font = 16, background = "white")
        #self.Text_for_save1.grid(row=0, column=0)
        self.listbox1 = Listbox(self,exportselection=0)
        self.listbox1.insert(END, u"常用列表")
        self.update_listbox1()            
        self.listbox1.grid(row=0, column=0)
        self.listbox1.bind('<<ListboxSelect>>',self.motion3)
        #images
        img = ImageTk.PhotoImage(file='1.PNG')
        
        self.lab1 = Label(self,text=u"照片顯示",image=img,height=489, width=489)
        self.lab1.grid(row=0, column=1, rowspan=3,columnspan=4)
        self.lab1.bind('<Button-1>',self.start)
        
        
        self.listbox2 = Listbox(self,exportselection=0)
        self.listbox2.insert(END, u"演員")
        self.listbox2.grid(row=1, column=0) 
        self.listbox2.bind('<<ListboxSelect>>',self.motion1)
        
        #get actors
        get_all_files = self.files_get.get_fileinfo(self.search_path)
        self.search_path2 = self.files_get.folder #save first root path
        count = 1
        for item,path in get_all_files.items():
            self.listbox2.insert(END, item)
            self.list_actor_name [count] = item
            count += 1
        #print(self.files_get.folder)
        
        self.listbox3 = Listbox(self,exportselection=0)
        self.listbox3.insert(END, u"作品")
        self.listbox3.grid(row=2, column=0) 
        self.listbox3.bind('<<ListboxSelect>>',self.motion2)
        #keep update window
        #self.after(1000, self.print_select)
        #self.button1 = Button(self,text="print",command=self.callback1)
        #self.button1.grid(row=3, column=0,) 
        #self.button2 = Button(self,text="start",command=self.callback2)
        #self.button2.grid(row=3, column=1) 
        
    def callback1(self):
        self.select_2=""
        self.movie_path = ""
        if self.select_1 != int(self.listbox2.curselection()[0]):
            self.select_1 = int(self.listbox2.curselection()[0]) #取taple[0]
        else:
            try:
                self.select_2 = int(self.listbox3.curselection()[0]) #取taple[0]
            except:
                self.select_2 = 0 
        
        # search from root
        #get_all_files = self.files_get.get_fileinfo(self.search_path)
        # second
        get_all_files = self.files_get.get_fileinfo(self.search_path2[self.list_actor_name[self.select_1]])
        self.current_select_act = self.list_actor_name[self.select_1]
        photos = self.files_get.photo
        self.movie_path = self.files_get.movie
        self.show_photo(photos)         
        
        #show works if selected
        if self.select_2 and self.select_2!=0:
            get_all_files = self.files_get.get_fileinfo(self.files_get.folder[self.list_works_name[self.select_2]])
            print(self.list_works_name[self.select_2])
            self.current_select_work = self.list_works_name[self.select_2]
            photos = self.files_get.photo
            self.movie_path = self.files_get.movie
            self.show_photo(photos)
        else:
            self.listbox3.delete(1, END) # clear
            self.listbox3_show(self.files_get.folder)
    def callback2(self):
        #self.update_listbox1()
        path_selected_favor = ""
        path = ""
        self.select_3 = int(self.listbox1.curselection()[0])
        selected_favor_name = self.list_favor_name[self.select_3]
        self.current_select_favor = selected_favor_name
        selected_favor_name = selected_favor_name.split("_")
        path_selected_favor = os.path.join(self.search_path,selected_favor_name[0],selected_favor_name[1])
        path = path_selected_favor
        get_all_files = self.files_get.get_fileinfo(path)
        photos = self.files_get.photo
        self.movie_path = self.files_get.movie
        self.show_photo(photos)
        #get_all_files = self.files_get.get_fileinfo([)

    def listbox3_show(self,lists):
        count = 1
        for item, path in lists.items():
            self.listbox3.insert(END, item)
            self.list_works_name[count] = item
            count += 1
        #print(self.files_get.folder)
    def show_photo(self,photo_update):
        for photo in photo_update:
            img_resize = Image.open(fp=photo).resize((489, 489)) #image.ANTIALIAS for best quality
            img = ImageTk.PhotoImage(img_resize)
            self.lab1.configure(image=img)
            self.lab1.image = img   # keep image
        #self.update_idletasks()
    def motion1(self,event):
        self.callback1()
    def motion2(self,event):
        self.callback1()
    def motion3(self,event):
        self.listbox2.selection_clear(self.select_1)
        self.listbox3.selection_clear(self.select_2)
        self.callback2()
    def start(self,event):
        if self.movie_path:
            #count when you play the movie
            movie_name = self.current_select_act+'_'+self.current_select_work  
            if movie_name =="_":
                print(self.current_select_favor)
                movie_name = self.current_select_favor 
                 
            if movie_name in self.faverit.keys():
                self.faverit[movie_name] = self.faverit[movie_name] + 1
            else:
                # add new
                self.faverit[movie_name] = 1
            #save favor
            with open(self.favor_file,'w') as f:
                f.writelines(str(self.faverit))
            #play movie    
            os.system(self.movie_path[0].decode('utf-8'))
    def update_listbox1(self):
        self.listbox1.delete(1, END) # clear
        #faverit
        try:
            with open(self.favor_file,'r') as f:
                #for line in f:
                favor_count = 1
                self.faverit = eval(f.readline())
                favor_sort = sorted(self.faverit.items(),key=operator.itemgetter(1), reverse=True)
                for favor in favor_sort:
                    self.listbox1.insert(END, favor[0])
                    self.list_favor_name[favor_count] = favor[0]
                    favor_count = favor_count + 1
                    if favor_count >= 5:
                        break
        except:
            print('no faverit')
            
if __name__ == '__main__':
    root = Tk() # Tk Object
    root.title("Video")
    app = DemoGUI(master=root)
    #start the program
    app.mainloop()
