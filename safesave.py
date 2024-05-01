import tkinter
import os
import tkinter.messagebox
import tkinter.filedialog
import shutil
import win10toast
def changefrom(labfrom:tkinter.Label):
    path=tkinter.filedialog.askdirectory(title="Dossier à sauvegarder")
    path=path.replace("/","\\")
    labfrom.config(text="Dossier à sauvegarder : "+path)
def changeto(labto:tkinter.Label):
    path=tkinter.filedialog.askdirectory(title="Dossier de destination")
    path=path.replace("/","\\")
    labto.config(text="Dossier de destination : "+path)
def save(labfrom:tkinter.Label,labto:tkinter.Label,butsave:tkinter.Button,state:tkinter.Label):
    pathfrom=labfrom.cget("text")[24::]
    pathto=labto.cget("text")[25::]
    pathto=str(pathto)
    pathfrom=str(pathfrom)
    if not os.path.exists(pathfrom):
        tkinter.messagebox.showerror(title="Chemin non existant",message="Le dossier à sauvegarder n'existe pas.\nSi il s'agit d'un périphérique de stockage externe, vérifier qu'il est bien connecté.")
        return
    if not os.path.exists(pathto):
        tkinter.messagebox.showerror(title="Chemin non existant",message="Le dossier de destination n'existe pas.\nSi il s'agit d'un périphérique de stockage externe, vérifier qu'il est bien connecté.")
        return
    if pathfrom.startswith(pathto) or pathto==pathfrom:
        tkinter.messagebox.showerror(title="Copie impossible",message="Ce type de sauvegarde est impossible.")
        return
    butsave.config(state="disabled")
    if tkinter.messagebox.askyesno(title="Voulez vous vraiment sauvegarder ?",message="Si vous continuer :\n - tout le contenu du dossier de destination sera supprimé\n - n'éteigner pas l'ordinateur pendant la sauvegarde"):
        state.config(text="Démarrage...")
        contentto=os.listdir(pathto)
        for i in range(len(contentto)):
            state.config(text="Suppression de "+pathto+"/"+contentto[i]+"...")
            if os.path.isfile(pathto+"/"+contentto[i]):
                os.remove(pathto+"/"+contentto[i])
            elif os.path.isdir(pathto+"/"+contentto[i]):
                try:
                    os.rmdir(pathto+"/"+contentto[i])
                except:
                    shutil.rmtree(pathto+"/"+contentto[i])
        state.config(text="Copie des fichiers...")
        contentfrom=os.listdir(pathfrom)
        for i in range(len(contentfrom)):
            state.config(text="Copie de "+pathfrom+"/"+contentfrom[i]+"...")
            if os.path.isfile(pathfrom+"/"+contentfrom[i]):
                shutil.copy(pathfrom+"/"+contentfrom[i],pathto+"/"+contentfrom[i])
            elif os.path.isdir(pathfrom+"/"+contentfrom[i]) and len(os.listdir(pathfrom+"/"+contentfrom[i]))==0:
                os.makedirs(pathto+"/"+contentfrom[i])
            elif os.path.isdir(pathfrom+"/"+contentfrom[i]) and len(os.listdir(pathfrom+"/"+contentfrom[i]))!=0:
                shutil.copytree(pathfrom+"/"+contentfrom[i],pathto+"/"+contentfrom[i])
        state.config(text="Prêt")
        butsave.config(state="active")
        notif=win10toast.ToastNotifier()
        notif.show_toast(title="Sauvegarde terminé",msg="SafeSave a terminé la sauvegarde de vos données.",duration=20,threaded=True)
    else:
        butsave.config(state="active")
def credits():
    tkinter.messagebox.showinfo("Crédits","Programme écrit et imaginé par lolo859.")
main=tkinter.Tk()
main.title("SafeSave v1.0")
main.geometry("600x200")
main.resizable(width=False,height=False)
labfrom=tkinter.Label(main,text="Dossier à sauvegarder : ",anchor="w")
labfrom.place(width=520,height=50,x=0,y=0)
butfrom=tkinter.Button(main,text="Parcourir",command=lambda:changefrom(labfrom))
butfrom.place(width=80,height=50,x=520,y=0)
labto=tkinter.Label(main,text="Dossier de destination : ",anchor="w")
labto.place(width=520,height=50,x=0,y=50)
butto=tkinter.Button(main,text="Parcourir",command=lambda:changeto(labto))
butto.place(width=80,height=50,x=520,y=50)
butsave=tkinter.Button(main,text="Sauvegarder",state="active",command=lambda:save(labfrom,labto,butsave,state))
butsave.place(width=300,height=50,x=0,y=100)
butcred=tkinter.Button(main,text="Crédits",command=credits)
butcred.place(width=300,height=50,x=300,y=100)
state=tkinter.Label(main,text="Prêt",anchor="center")
state.place(width=600,height=50,x=0,y=150)
main.mainloop()