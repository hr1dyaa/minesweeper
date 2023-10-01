import random
import csv



class Minesweeper:
    def __init__(self):
        self.m=[]
        self.flag=0
    def clicked(self,a):
        if self.flag==0:
            self.flag=1
            self.mine=[]
            for i in range(16):
                self.m.append([])
                for j in range(30):
                    self.m[i].append(0)
                    self.mine.append((i,j))
            inp=(int(a[0:a.index(',')]),int(a[a.index(',')+1:len(a)]))
            self.mine.remove(inp)
            for i in range(380):
                self.mine.remove(random.choice(self.mine))
            for i in self.mine:
                self.m[i[0]][i[1]]='M'
            for i in range(16):
                for j in range(30):
                    if self.m[i][j]==0:
                        c=0
                        search=set([(i,j-1),(i,j+1),(i+1,j),(i+1,j+1),(i+1,j-1),(i-1,j-1),(i-1,j),(i-1,j+1)])
                        if i==0:
                            search=search.difference(set([(i-1,j),(i-1,j-1),(i-1,j+1)]))
                        if j==0:
                            search=search.difference(set([(i,j-1),(i-1,j-1),(i+1,j-1)]))
                        if i==15:
                            search=search.difference(set([(i+1,j),(i+1,j-1),(i+1,j+1)]))
                        if j==29:
                            search=search.difference(set([(i,j+1),(i-1,j+1),(i+1,j+1)]))
                        for k in search:
                            if self.m[k[0]][k[1]]=='M':
                                c+=1
                        self.m[i][j]=c       
            f=open('mine.csv','w')
            write=csv.writer(f)
            for i in self.m:
                write.writerow(i)
        return self.m[int(a[0:a.index(',')])][int(a[a.index(',')+1:len(a)])]