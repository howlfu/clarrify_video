'''
Created on 2017年4月6日

@author: HL
'''
#coding=utf-8
from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image
from Get_dir_info import dir_files
import os
import operator

class DemoGUI(Frame):
    select_1= 0 #favor
    select_2= 0 #actor
    select_3= 0 #works
    files_get = object
    search_path = {}
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
    mainHi = 619
    mainWi = 840
    upHi = 80
    upWi = mainWi +173 # small bar
    colspan1 = 2
    colspan2 = 10
    barcolspan = colspan1 +colspan2
    imagebar_count = 0
    def __init__(self, master=None):
        Frame.__init__(self, master)
        #self.search_path = 'D:\GitHub\movies'
        self.files_get = dir_files()
        self.grid()
        self["background"] = "gray"
        search_path = {}
        if not os.path.exists(self.favor_file):
            search_path[1]=  filedialog.askdirectory()
            self.search_path = search_path[1]
            with open(self.favor_file,'w') as f:
                favor = str(self.faverit) + "\n"
                f.writelines(favor)
                f.writelines(str(self.search_path))
        else:
            with open(self.favor_file,'r') as f:
                #for line in f:
                self.faverit = eval(f.readline())
                search_path = eval(f.readline())
                self.search_path = search_path[1]
        self.createWidgets()
        
    def createWidgets(self):
        #index
        #self.Text_for_save1 = Label(self, text = u"預覽圖", font = 16, background = "white")
        #self.Text_for_save1.grid(row=0, column=0)
        image = ImageTk.PhotoImage('RGB', (self.upHi,self.upWi))
        self.lab1 = Label(self,text=u"作品顯示bar",image=image,height=self.upHi, width=self.upWi,)
        self.lab1.grid(row=0, column=0,columnspan=self.barcolspan)
        
        self.listbox1 = Listbox(self,exportselection=0, width= 24)
        self.listbox1.insert(END, u"常用列表")
        self.listbox1.itemconfig(0,{'bg':'lemon chiffon'})
        self.listbox1.grid(row=2, column=0, columnspan=self.colspan1)
        self.update_listbox1()#favor 
        self.listbox1.bind('<<ListboxSelect>>',self.motion3)
        #images
        #img = ImageTk.PhotoImage(file='1.PNG')
        pimage = ImageTk.PhotoImage('RGB', (self.mainWi,self.mainHi))
        self.lab2 = Label(self,text=u"照片顯示",image=pimage,height=self.mainHi, width=self.mainWi)
        
        self.lab2.grid(row=2, column=2, rowspan=3,columnspan=self.colspan2)
        self.lab2.bind('<Button-1>',self.start)
        
        
        self.listbox2 = Listbox(self,exportselection=0, width= 24, height= 18)
        self.listbox2.insert(END, u"演員", )
        self.listbox2.grid(row=3, column=0,columnspan=self.colspan1) 
        self.listbox2.itemconfig(0,{'bg':'lemon chiffon'})
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
        
        self.listbox3 = Listbox(self,exportselection=0,  width= 24)
        self.listbox3.insert(END, u"作品")
        self.listbox3.itemconfig(0,{'bg':'lemon chiffon'})
        self.listbox3.grid(row=4, column=0,columnspan=self.colspan1) 
        self.listbox3.bind('<<ListboxSelect>>',self.motion2)
        #keep update window
        #self.after(1000, self.print_select)
        #self.button1 = Button(self,text="print",command=self.callback1)
        #self.button1.grid(row=3, column=0,) 
        #self.button2 = Button(self,text="start",command=self.callback2)
        #self.button2.grid(row=3, column=1) 
        
    def callback1(self):
        self.select_3=""
        self.movie_path = ""
        if int(self.listbox2.curselection()[0]) == 0:
            # clear works when select actor list 0
            self.listbox3.delete(1, END) 
            
        if self.select_2 != int(self.listbox2.curselection()[0]):
            self.select_2 = int(self.listbox2.curselection()[0]) #取taple[0]
        else:
            try:
                self.select_3 = int(self.listbox3.curselection()[0]) #取taple[0]
            except:
                self.select_3 = 0 
        
        # search from root
        #get_all_files = self.files_get.get_fileinfo(self.search_path)
        # second
        if int(self.listbox2.curselection()[0]) == 0:
            self.listbox3.delete(1, END) # clear
        else:
            
            get_all_files = self.files_get.get_fileinfo(self.search_path2[self.list_actor_name[self.select_2]])
            self.current_select_act = self.list_actor_name[self.select_2]
            photos = self.files_get.photo
            
            self.show_main_photo(photos)         
            
            #show works if selected
            if self.select_3 and self.select_3!=0:
                #show image when select
                get_all_files = self.files_get.get_fileinfo(self.files_get.folder[self.list_works_name[self.select_3]])
                self.current_select_work = self.list_works_name[self.select_3]
                photos = self.files_get.photo
                self.movie_path = self.files_get.movie
                self.show_main_photo(photos)
            else:
                #clean if no listbox3 and regenerate list box3
                self.movie_path = self.files_get.movie
                self.listbox3.delete(1, END) # clear
                self.listbox3_show(self.files_get.folder)
                self.imagebar_show(self.files_get.folder)
        
    def callback2(self):
        #self.update_listbox1()
        path_selected_favor = ""
        path = ""
        self.select_1 = int(self.listbox1.curselection()[0])
        selected_favor_name = self.list_favor_name[self.select_1]
        self.current_select_favor = selected_favor_name
        selected_favor_name = selected_favor_name.split("_")
        path_selected_favor = os.path.join(self.search_path,selected_favor_name[0],selected_favor_name[1])
        path = path_selected_favor
        get_all_files = self.files_get.get_fileinfo(path)
        photos = self.files_get.photo
        self.movie_path = self.files_get.movie
        self.show_main_photo(photos)
        #get_all_files = self.files_get.get_fileinfo([)

    def listbox3_show(self,lists):
        count = 1
        for item, path in lists.items():
            self.listbox3.insert(END, item)
            self.list_works_name[count] = item
            count += 1
            #show image bar
            
    def imagebar_show(self,lists):
        self.clear_imgbar()
        count = 0
        self.imagebar_count = 0
        for item, path in lists.items():
            #paint all the works
            if count > 11:
                #only show 12 images
                break
            get_all_files = self.files_get.get_fileinfo(path)
            photos = self.files_get.photo
            photo = photos[0]
            img_resize = Image.open(fp=photo).resize((self.upHi, self.upHi)) #image.ANTIALIAS for best quality
            img = ImageTk.PhotoImage(img_resize)
            lab_in_imagebar = 'lab' + str(count)
            #callback = # image call back
            self.lab_in_imagebar = Label(self,text=u"作品顯示bar",image=img,height=self.upHi, width=self.upHi,)
            #save the name
            self.lab_in_imagebar.my_name = photo
            
            self.lab_in_imagebar.image = img   # keep image

            self.lab_in_imagebar.grid(row=0, column=count)
            self.lab_in_imagebar.bind('<Button-1>',self.motion4)
            self.lab_in_imagebar.bind('<Double-Button-1>',self.motion5)
        
            count = count + 1
            self.lab_in_imagebar.selected = count
            self.imagebar_count = count
            
        while count < 12:
            #paint all the empty for 12 pictures
            image = ImageTk.PhotoImage('RGB', (self.upHi,self.upHi))
            self.lab_in_imagebar = Label(self,text=u"作品顯示bar",image=image,height=self.upHi, width=self.upHi,)
            self.lab_in_imagebar.grid(row=0, column=count)
            count = count + 1
            
            
        
        #print(self.files_get.folder)
    def show_main_photo(self,photo_update):
        for photo in photo_update:
            img_resize = Image.open(fp=photo).resize((self.mainWi, self.mainHi)) #image.ANTIALIAS for best quality
            img = ImageTk.PhotoImage(img_resize)
            self.lab2.configure(image=img)
            self.lab2.image = img   # keep image
        
        #self.update_idletasks()
    def motion1(self,event):
        #actor
        self.callback1()
    def motion2(self,event):
        #works
        if self.select_1:
            self.listbox1.selection_clear(self.select_1)
        self.callback1()
    def motion3(self,event):
        #favor
        
        if self.select_3:
            self.listbox3.selection_clear(self.select_3)
        #self.clear_imgbar()
        self.callback2()
    def motion4(self,event):
        #one click on image bar
        event_name = []
        event_name.append(event.widget.my_name) 
        
        #clear listbox3 before set
        if self.select_1:
            self.listbox1.selection_clear(self.select_1)
        if self.select_3:
            self.listbox3.selection_clear(self.select_3)
        #save current image bar selected
        self.select_3 = event.widget.selected
        self.current_select_work = self.list_works_name[self.select_3]
        #select listbox3 when select imagebar
        
        self.listbox3.select_set(self.select_3)
        #make path for each image bar label
        path_selected = os.path.join(self.search_path,self.current_select_act,self.current_select_work)
        get_all_files = self.files_get.get_fileinfo(path_selected)
        self.movie_path = self.files_get.movie
        self.callback3(event_name) 
    def motion5(self,event):
        #double clicks
        self.start(event)    
    def start(self,event):
        if self.movie_path:
            #count when you play the movie
            movie_name = self.current_select_act+'_'+self.current_select_work  
            print(movie_name)  
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
                favor = str(self.faverit) + "\n"
                serch_path = {}
                serch_path[1] = self.search_path
                f.writelines(favor)
                f.writelines(str(serch_path))
                print("search path = " + str(serch_path))
            #play movie    
            os.system(self.movie_path[0].decode('utf-8'))
    def update_listbox1(self):
        self.listbox1.delete(1, END) # clear
        #faverit
        favor_count = 1
        favor_sort = sorted(self.faverit.items(),key=operator.itemgetter(1), reverse=True)
        for favor in favor_sort:
            self.listbox1.insert(END, favor[0])
            self.list_favor_name[favor_count] = favor[0]
            favor_count = favor_count + 1
            if favor_count > 5:
                break
    def clear_imgbar(self):
        image = ImageTk.PhotoImage('RGB', (self.upHi,self.upWi))
        self.lab1 = Label(self,text=u"作品顯示bar",image=image,height=self.upHi, width=self.upWi,)
        self.lab1.grid(row=0, column=0,columnspan=self.barcolspan)
        
    def callback3(self, photo):  
        self.show_main_photo(photo)
            
if __name__ == '__main__':
    root = Tk() # Tk Object
    root.title("Video")
    app = DemoGUI(master=root)
    #start the program
    app.mainloop()
