'''
Created on 2017年4月5日

@author: HL
'''
#coding=utf-8
import os

class dir_files(object):
    '''
    1. make object
    path = path you want
    obj = dir_files(path)
    2.use get_fileinfo to get path and all files
    3.get photo and movie and folder
    '''
    get_path = ""
    photo = []
    movie = []
    folder = {}
    dircount =0
    def __init__(self, path_of_photo = ''):
        self.get_path = path_of_photo
    def __str__(self, *args, **kwargs):
        string = self.get_path + " have already been classified."
        return string
    def get_fileinfo(self, path_info=""):
        self.folder = {}
        self.get_path = path_info
        self.photo = []
        self.movie = []
        self.dircount = 0
        try:
            filenames = os.listdir(self.get_path)
            for file in filenames:
                path = os.path.join(self.get_path,file)
                if self.is_image(path):
                    #print('get image and movie: ' + path)
                    self.photo.append(path)
                elif self.is_video(path):
                    path = path.encode('utf-8')
                    self.movie.append(path)
                else:
                    #dir
                    if os.path.isdir(path):
                        self.dircount = self.dircount+1
                        self.folder[file] = path
        except:
            #no path
            pass
        return self.folder
                
    def is_image(self,img_file):
        text = os.path.splitext(img_file)[-1]
        return text in ['.jpg','.JPG','.png','.PNG']
    
    def is_video(self,img_file):
        text = os.path.splitext(img_file)[-1]
        return text in ['.MOV','.mov','.mp4','.MP4','.mkv','.MKV','.AVI','.avi','.RMVB','.rmvb']
            
if __name__ == '__main__':
    test = dir_files()
    info1 = {}
    info1 = test.get_fileinfo('D:\\GitHub\\movies\\周杰倫\\葉惠美')
    print("img = " + str(test.photo))
    print("mov = " + str(test.movie))
    #print(info1)
    #for path2 in info1.values():
    #    info2 = test.get_fileinfo(path2)
    #    print("img = " + str(test.photo))
    #    print("mov = " + str(test.movie))
    #    for path3 in info2.values():
    #        info3 = test.get_fileinfo(path3)

    
    