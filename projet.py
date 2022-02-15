from tkinter import *  # importe la bibliotheque tkinter
from tkinter import filedialog,messagebox#importe messagebox et filedialog
from tkinter.ttk import Treeview # pour le tableau
from PIL import Image, ImageTk # pour le fond d'écran
from matplotlib.figure import Figure # pour afficher figure (la fênetre du graphe)
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg) # pour creer l'histogramme dans la figure
import sqlite3 # utilisation d'une base de donnees
from datetime import date # recuperer la date d'aujourd'hui
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph # creation d'un texte pdf
from reportlab.lib.styles import getSampleStyleSheet #mise en place d'un font pour le pdf

base = sqlite3.connect('personnel.db')#connection base de donnees
database = base.cursor() # mise en place d'un curseur pour recuperer les donnees
fenPrincipale = Tk()  # cree une fenetre
fenPrincipale.title("GesMag")  # titre de la fenetre
fenPrincipale.geometry("800x400")  # taille de la fenetre
fenPrincipale.resizable(False, False) # bloquer le redimensionnement de la fenetre
fenPrincipale.configure(bg='white') # couleur background window
contenu=Frame(fenPrincipale) # creation frame
numero_fen=0 # recuperation de la fenetre afficher
status=""# grade de la personne connecter (caisier ou manager)

def new_frame(): # celà permet de crée une Frame dans la fênetre et qui sera ensuite écraser par la prochaine quand j'ouvrirais une autre Frame.
    global contenu
    contenu.destroy()
    contenu=Frame(fenPrincipale)

def affiche(): # les paramêtre d'affichage des caisier
    fenPrincipale.geometry("800x400") # redimensionnement fenetre
    new_frame()
    contenu.configure(width=801,height=401) # redimensionnement frame principale
    global numero_fen
    image = Image.open("./images.png")# ouvertuere de l'image de fond d'ecran
    resize_image = image.resize((801, 401)) # redimensionnement image fond d'ecran
    img = ImageTk.PhotoImage(resize_image) # le rendre adaptable a du tkinter
    a = Label(contenu, image=img)
    a.image = img
    a.place(x=-1,y=-1)# mise en place fond d'ecran
    global numero_fen
    numero_fen=3
    fenPrincipale.title("chercher caisier")  # titre de la fenetre

    idn = StringVar()# variable

    Label(contenu,text="Search seller",bg='black',fg='white',font=("Courier", 30, "italic","bold")).place(x=225,y=10)
    Label(contenu,text="Enter ID",bg='black',fg='white',font=("Arial", 15, "italic","bold")).place(x=100,y=105)
    ids=Entry(contenu,textvariable=idn,width=20,bg='black',fg='white',font=("Comic sans ms", 20, "italic","bold"))# entree de l'ID de la personne rechercher
    ids.place(x=200,y=100)# mise en place entree
    
    def vider():# pour vider entree
        ids.delete(0,"end")
    def entree(_event):# ça cherche quand on presse Entrée
        search()
    
    def show():#afficher tout les utilisateur
        fen = Toplevel()  # cree une fenetre
        fen.grab_set() #pour intéragir avec qu'une fênetre à la fois
        fen.title("afficher tout les caisier")  # titre de la fenetre
        fen.geometry("800x400")  # taille de la fenetre
        fen.resizable(False, False) 
        fen.configure(bg='white')#couleur background window
        cb=Frame(fen)
        cb.configure(width=801,height=401)
        image = Image.open("./images.png")
        resize_image = image.resize((801, 801))
        img = ImageTk.PhotoImage(resize_image)
        ab = Label(cb, image=img)
        ab.image = img
        ab.place(x=-1,y=-1)
        def ret():# intéragir de nouveau avec la fênetre principale
            fen.grab_release()
            fen.destroy()
        scframe=Frame(fen,height=400)
        tableau = Treeview(scframe,height=14, columns=('username', 'name', 'first name','date of birth','address','post code','login','password'))#creation tableau
        
        #parametrage des colonne
        tableau.column('username', width = 90)
        tableau.column('name', width = 75)
        tableau.column('first name', width = 100)
        tableau.column('date of birth', width = 110)
        tableau.column('address', width = 80)
        tableau.column('post code', width = 90)
        tableau.column('login', width = 75)
        tableau.column('password', width = 90)

        #affiche des nom des colonne
        tableau.heading('username', text='Username')
        tableau.heading('name', text='Name')
        tableau.heading('first name', text='First name')
        tableau.heading('date of birth', text='Date of birth')
        tableau.heading('address', text='Address')
        tableau.heading('post code', text='Post code')
        tableau.heading('login', text='Login')
        tableau.heading('password', text='Password')
        tableau['show'] = 'headings'

        for i in database.execute("SELECT * FROM liste"):# insert des donnees des utilisateur
            tableau.insert('',END, values=i)
        tableau.pack(side = LEFT, fill=BOTH)# mise en place tableau
        scroll = Scrollbar(scframe,width=15,orient=VERTICAL,command=tableau.yview)# mise en place scroll bar
        scroll.pack(side = RIGHT, fill=BOTH)
        cb.place(x=-1,y=-1)

        scframe.place(x=40,y=10)
        fenbtn = Button(fen, text="Return",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=ret).place(x=300,y=325)#creation button pour quitter la fenetre
        fen.mainloop()
    

    us=StringVar()
    na=StringVar()
    fa=StringVar()
    da=StringVar()
    ad=StringVar()
    pc=StringVar()
    lo=StringVar()
    pw=StringVar()
    Label(contenu, textvariable = us,bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=90, y=150)
    Label(contenu, textvariable = na,bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=90, y=190)
    Label(contenu, textvariable = fa,bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=90, y=230)
    Label(contenu, textvariable = da,bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=90, y=270)
    Label(contenu, textvariable = ad,bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=400, y=150)
    Label(contenu, textvariable = pc,bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=400, y=190)
    Label(contenu, textvariable = lo,bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=400, y=230)
    Label(contenu, textvariable = pw,bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=400, y=270)
    def search():
        for i in database.execute("SELECT * FROM liste WHERE ID='%s'"% idn.get()):#recuperation des donees en fonction de l'ID si disponible
            us.set(value="username: "+str(i[0]))
            na.set(value="name: "+str(i[1]))
            fa.set(value="first name: "+str(i[2]))
            da.set(value="date of birth: "+str(i[3]))
            ad.set(value="address: "+str(i[4]))
            pc.set(value="post code: "+str(i[5]))
            lo.set(value="login: "+str(i[6]))
            pw.set(value="password: "+str(i[7]))
            return
        messagebox.showwarning("Error","This seller doesn't exist")

    fenbtn = Button(contenu, text="Clear",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=vider).place(x=50,y=325)#creation button
    fenbtn = Button(contenu, text="Search",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=search).place(x=600,y=95)#creation button
    fenbtn = Button(contenu, text="Show all",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=show).place(x=300,y=325)#creation button
    fenbtn = Button(contenu, text="Return",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=manage).place(x=550,y=325)#creation button
    ids.bind('<Return>', entree)
    contenu.place(x=-1,y=-1)

def manage(): # creation interface de management
    fenPrincipale.geometry("800x400")
    new_frame()
    global contenu
    contenu.configure(width=801,height=401)
    global numero_fen
    image = Image.open("./images.png")
    resize_image = image.resize((801, 401))
    img = ImageTk.PhotoImage(resize_image)
    a = Label(contenu, image=img)
    a.image = img
    a.place(x=-1,y=-1)
    numero_fen=1
    fenPrincipale.title("Interface Manager")
    Label(contenu,text="Management",bg='black',fg='white',font=("Courier", 30, "italic","bold")).place(x=275,y=10)
    Button(contenu, text="Add seller",width=25,fg='white',bg='black',font=("Courier", 20, "italic"), command=ajout).place(x=200,y=60)# creation boutton
    Button(contenu, text="afficher caissier",width=25,fg='white',bg='black',font=("Courier", 20, "italic"), command=affiche).place(x=200,y=110)# creation boutton
    Button(contenu, text="supprimer caissier",width=25,fg='white',bg='black',font=("Courier", 20, "italic"), command=supp).place(x=200,y=160)# creation boutton
    Button(contenu, text="suivi vente",width=25,fg='white',bg='black',font=("Courier", 20, "italic"), command=suivi).place(x=200,y=210)# creation boutton
    Button(contenu, text="fonctionalites caissier",width=25,fg='white',bg='black',font=("Courier", 20, "italic"), command=lambda a=[]:fonc(a)).place(x=200,y=260)# creation boutton
    Button(contenu, text="Add stock",width=25,fg='white',bg='black',font=("Courier", 20, "italic"), command=add_stock).place(x=200,y=310)# creation boutton
    Button(contenu, text="Log out",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=login).place(x=620,y=350)# creation boutton
    contenu.place(x=-1,y=-1)

def add_stock(): #création de l'interface d'ajout dans le stocks des produits
    fenPrincipale.geometry("1400x500")
    new_frame()
    global contenu
    contenu.configure(width=1401,height=501)
    global numero_fen
    image = Image.open("./images.png")
    resize_image = image.resize((1401, 501))
    img = ImageTk.PhotoImage(resize_image)
    a = Label(contenu, image=img)
    a.image = img
    listebut=[]
    a.place(x=-1,y=-1)
    fenPrincipale.title("Ajouter au stock")
    scframe=Frame(contenu,height=300,width=1)
    scframe2=Frame(contenu,height=500,width=1)
    scframe3=Frame(contenu,height=300,width=1)
    scframe4=Frame(contenu,height=500,width=1)
    def cree(text,text2,text3,text4):
        liste_cat=["fruits et legumes","boulangerie","boucherie et poissonnerie","entretien"]
        for i in database.execute("SELECT NAME,IMAGE,ID,STOCK FROM article WHERE CATEGORIE='%s'"% liste_cat[0]):# insertion dans le texte numero 1 des articles fruits legumes
            image = Image.open(i[1])
            resize_image = image.resize((80, 80))
            img = ImageTk.PhotoImage(resize_image)
            lab=Label(text, image = img)
            lab.image=img
            text.window_create(END, window= lab)
            text.insert("end", i[0]+"\t")
            stck=IntVar(value=i[3])
            lab1=Label(text, textvariable=stck)
            text.window_create(END, window= lab1)
            text.insert("end", "\t")
            listebut[i[2]-1].config(command = lambda a=i[0],b=stck:add(a,b))
            text.window_create("end", window=listebut[i[2]-1])# ajout d'un boutton dans le texte
            text.insert("end", "\n")
        for i in database.execute("SELECT NAME,IMAGE,ID,STOCK FROM article WHERE CATEGORIE='%s'"% liste_cat[1]):# insertion dans le texte numero 2 des articles de la boulangerie
            image = Image.open(i[1])
            resize_image = image.resize((80, 80))
            img = ImageTk.PhotoImage(resize_image)
            lab=Label(text2, image = img)
            lab.image=img
            text2.window_create(END, window= lab)
            text2.insert("end", i[0]+"\t")
            stck=IntVar(value=i[3])
            lab1=Label(text2, textvariable=stck)
            text2.window_create(END, window= lab1)
            text2.insert("end", "\t")
            listebut[i[2]-1].config(command = lambda a=i[0],b=stck:add(a,b))
            text2.window_create("end", window=listebut[i[2]-1]) # ajout d'un boutton dans le texte
            text2.insert("end", "\n")
        for i in database.execute("SELECT NAME,IMAGE,ID,STOCK FROM article WHERE CATEGORIE='%s'"% liste_cat[2]):# insertion dans le texte numero 3 des articles boucherie poissonerie
            image = Image.open(i[1])
            resize_image = image.resize((100, 100))
            img = ImageTk.PhotoImage(resize_image)
            lab=Label(text3, image = img)
            lab.image=img
            text3.window_create(END, window= lab)
            text3.insert("end", i[0]+"\t")
            stck=IntVar(value=i[3])
            lab1=Label(text3, textvariable=stck)
            text3.window_create(END, window= lab1)
            text3.insert("end", "\t")
            listebut[i[2]-1].config(command = lambda a=i[0],b=stck:add(a,b))
            text3.window_create("end", window=listebut[i[2]-1]) # ajout d'un boutton dans le texte
            text3.insert("end", "\n")
        for i in database.execute("SELECT NAME,IMAGE,ID,STOCK FROM article WHERE CATEGORIE='%s'"% liste_cat[3]):# insertion dans le texte numero 4 des produits d'entretien
            image = Image.open(i[1])
            resize_image = image.resize((100, 100))
            img = ImageTk.PhotoImage(resize_image)
            lab=Label(text4, image = img)
            lab.image=img
            text4.window_create(END, window= lab)
            text4.insert("end", i[0]+"\t")
            stck=IntVar(value=i[3])
            lab1=Label(text4, textvariable=stck)
            text4.window_create(END, window= lab1)
            text4.insert("end", "\t")
            listebut[i[2]-1].config(command = lambda a=i[0],b=stck:add(a,b))
            text4.window_create("end", window=listebut[i[2]-1]) # ajout d'un boutton dans le texte
            text4.insert("end", "\n")
        text.config(state='disabled')
        text2.config(state='disabled')
        text3.config(state='disabled')
        text4.config(state='disabled')
    Label(contenu,text="fruits et legumes",bg='black',fg='white',font=("Courier", 20, "italic","bold")).place(x=20,y=20)
    Label(contenu,text="boulangerie",bg='black',fg='white',font=("Courier", 20, "italic","bold")).place(x=400,y=20)
    Label(contenu,text="boucherie et poissonnerie",bg='black',fg='white',font=("Courier", 20, "italic","bold")).place(x=660,y=20)
    Label(contenu,text="produit d'entretien",bg='black',fg='white',font=("Courier", 20, "italic","bold")).place(x=1080,y=20)
    text = Text(scframe,height=13,width=21,font=("Courier", 15, "italic","bold"))
    text.insert("end", "Image"+"\t"+"Name"+"\t"+"Stock"+"\n")
    text.pack(side = LEFT,fill=BOTH)
    scroll = Scrollbar(scframe,width=15,orient=VERTICAL)
    scroll.pack(side = RIGHT,fill=BOTH)
    text2 = Text(scframe2,height=13,width=31,font=("Courier", 15, "italic","bold"))
    text2.insert("end", "Image"+"\t"+"Name"+"\t"+"Stock"+"\n")
    text2.pack(side = LEFT,fill=BOTH)
    scroll2 = Scrollbar(scframe2,width=15,orient=VERTICAL)
    scroll2.pack(side = RIGHT,fill=BOTH)
    text3 = Text(scframe3,height=13,width=25,font=("Courier", 15, "italic","bold"))
    text3.insert("end", "Image"+"\t"+"Name"+"\t"+"Stock"+"\n")
    text3.pack(side = LEFT,fill=BOTH)
    scroll3 = Scrollbar(scframe3,width=15,orient=VERTICAL)
    scroll3.pack(side = RIGHT,fill=BOTH)
    text4 = Text(scframe4,height=13,width=30,font=("Courier", 15, "italic","bold"))
    text4.insert("end", "Image"+"\t"+"Name"+"\t"+"Stock"+"\n")
    text4.pack(side = LEFT,fill=BOTH)
    scroll4 = Scrollbar(scframe4,width=15,orient=VERTICAL)
    scroll4.pack(side = RIGHT,fill=BOTH)
    def add(name,var): # ajout de +1 au stock en fonction du nom
        var.set(var.get()+1)
        database.execute("UPDATE article SET STOCK = ? WHERE NAME = ?",(var.get(),name))
        base.commit()
    for i in database.execute("SELECT NAME,CATEGORIE FROM article"): # creation de liste de bouttons
        if i[1]=="fruits et legumes":
            a=text
        if i[1]=="boulangerie":
            a=text2
        if i[1]=="boucherie et poissonnerie":
            a=text3
        if i[1]=="entretien":
            a=text4
        button = Button(a, text="add")
        listebut.append(button)
    cree(text,text2,text3,text4)
    text.config(yscrollcommand=scroll.set)
    scroll.config(command=text.yview)
    text2.config(yscrollcommand=scroll2.set)
    scroll2.config(command=text2.yview)
    text3.config(yscrollcommand=scroll3.set)
    scroll3.config(command=text3.yview)
    text4.config(yscrollcommand=scroll4.set)
    scroll4.config(command=text4.yview)
    scframe.place(x=10,y=110)
    scframe2.place(x=290,y=110)
    scframe3.place(x=690,y=110)
    scframe4.place(x=1020,y=110)
    fenbtn = Button(contenu, text="Return",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=manage).place(x=620,y=425) # creation de bouttons
    contenu.place(x=-1,y=-1)

def supp():# creation d'interface de suppression d'un utilisateur
    fenPrincipale.geometry("800x400")
    new_frame()
    contenu.configure(width=801,height=401)
    global numero_fen
    image = Image.open("./images.png")
    resize_image = image.resize((801, 401))
    img = ImageTk.PhotoImage(resize_image)
    a = Label(contenu, image=img)
    a.image = img
    a.place(x=-1,y=-1)
    global numero_fen
    numero_fen=3
    fenPrincipale.title("suprimer caisier")  # titre de la fenetre

    idn = StringVar()

    Label(contenu,text="Search seller",bg='black',fg='white',font=("Courier", 30, "italic","bold")).place(x=225,y=10)
    Label(contenu,text="Enter ID",bg='black',fg='white',font=("Arial", 15, "italic","bold")).place(x=100,y=105)
    ids=Entry(contenu,textvariable=idn,width=20,bg='black',fg='white',font=("Comic sans ms", 20, "italic","bold")) # entree de l'id d'un utilisateur
    ids.place(x=200,y=100)
    def vider():# suppression du contenu de l'entree
        ids.delete(0,"end")
    def entree(_event):
        delete()
    def delete():# suppression de l'utilisateur
        dele=False
        for i in database.execute("SELECT * FROM liste WHERE ID='%s'"% ids.get()): # pour savoir si l'id existe dans la database
            dele=True
        if dele: # si l'entree existe il le suprrimer et affiche un message qu'il est bien supprimer
            database.execute("DELETE FROM liste WHERE ID='%s'"% ids.get())
            base.commit()
            messagebox.showinfo("delete seller","the seller sucessfuly delete")
        else:# sinon il envoie un message d'erreur que l'entree a supprimer n'existe pas
            messagebox.showwarning("Error","the seller doesn't exist")
    fenbtn = Button(contenu, text="Clear",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=vider).place(x=125,y=325)#creation button
    fenbtn = Button(contenu, text="Delete",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=delete).place(x=600,y=95)#creation button
    fenbtn = Button(contenu, text="Return",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=manage).place(x=475,y=325)#creation button
    ids.bind('<Return>', entree)
    contenu.place(x=-1,y=-1)

def resultat(liste,total):#affiche un resumer du contenu du panier avant de les acheter
    fenPrincipale.geometry("350x400")
    new_frame()
    global contenu
    contenu.configure(width=351,height=401)
    global numero_fen
    image = Image.open("./images.png")
    resize_image = image.resize((351, 401))
    img = ImageTk.PhotoImage(resize_image)
    a = Label(contenu, image=img)
    a.image = img
    a.place(x=-1,y=-1)
    Label(contenu,text="RESUMER",bg='black',fg='white',font=("Courier", 20, "italic","bold")).place(x=115,y=10)
    scframe=Frame(contenu,height=500,width=1)
    text = Text(scframe,height=13,width=40,font=("Arial", 10, "italic","bold"))
    scroll = Scrollbar(scframe,width=15,orient=VERTICAL)
    text.config(yscrollcommand=scroll.set)
    scroll.pack(side = RIGHT,fill=BOTH)
    Label(contenu,text="TOTAL: "+str(total),bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=100,y=275)
    text.pack(side = LEFT,fill=BOTH)
    text.delete('1.0', END)
    text.insert("end","ID"+"\t"+"NOM"+"\t"+"PRIX"+"\t"+"QUANT"+"\t"+"TOTAL")
    for r in liste:
        for i in database.execute("SELECT ID,NAME,PRICE FROM article WHERE NAME='%s'"% r[0]):#insertion du contenu du panier dans le text
            text.insert("end", "\n"+str(i[0])+"\t"+str(i[1])+"\t"+str(i[2])+"\t"+str(r[1])+"\t"+str(round((r[1]*i[2]),2)))
    text.configure(state='disabled')
    scroll.config(command=text.yview)
    scframe.place(x=30,y=50)
    def action():#validation de l'achat 
        for r in liste:
            for i in database.execute("SELECT STOCK FROM article WHERE NAME='%s'"% r[0]):#mise a jour du stock de chaque article
                if not i[0]==0:
                    database.execute("UPDATE article SET STOCK = ? WHERE NAME = ?",((i[0]-r[1]),r[0]))
                    base.commit()
        change=False
        for i in database.execute("SELECT DATE,TOTAL FROM vente"):#mise a jour du total des vente du jour
            if i[0]==str(date.today()):
                change=True
                database.execute("UPDATE vente SET TOTAL = ? WHERE DATE = ?",(round((i[1]+total),2),i[0]))
                base.commit()
        if not change:
            b1=round(total,2)
            b2=str(date.today())
            a1=0
            a2=""
            lie= selectSql = [(idx, tlt,dat) for (idx, tlt,dat) in database.execute("SELECT * FROM vente ORDER BY ID DESC")]
            for r in lie:
                a1=r[1]
                a2=r[2]
                database.execute("UPDATE vente SET TOTAL = ?, DATE= ? WHERE ID = ?",(b1,b2,r[0]))
                base.commit()
                b1=a1
                b2=a2        
        prt = messagebox.askquestion ( title = "ACHAT EFFETUER " , message = "Voulez vous un reçu?" )#message demande ticket resumer
        if prt == "yes" :
            title = 'Reçu'
            textlines=[]
            count=0
            for i in text.get("1.0","end-1c"):
                if i=="\n":
                    count=count+1
            for i in range(0,count+1):
                textlines.append("")
            count=0
            for i in text.get("1.0","end-1c"):
                if i=="\n":
                    count=count+1
                elif i=="\t":
                    textlines[count]=textlines[count]+"\t"
                else:
                    textlines[count]=textlines[count]+i
            data=[]
            varline=[]
            newcount=0
            count=0
            for i in textlines:
                for r in i:
                    if r=="\t":
                        varline.append(i[newcount:count])
                        newcount=count+1
                    count=count+1
                varline.append(i[newcount:count])
                data.append(varline)
                varline=[]
                count=0
                newcount=0
            stylesheet = getSampleStyleSheet()
            doc = SimpleDocTemplate("reçu.pdf")
            headname = '<font>' + "Reçu" + "</font>"
            elements = []
            data.append("-------------------------")
            data.append(["TOTAL","","","",str(total)])
            t=Table(data)
            elements.append(Paragraph(headname, stylesheet["Title"]))
            elements.append(t)
            doc.build(elements)#creation d'un pdf avec le contenu acheter
            fonc([])
        if prt == "no" :
            fonc([])
        
    Button(contenu, text="Annuler",width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=lambda a=liste:fonc(a)).place(x=180,y=310)#creation boutton
    Button(contenu, text="Valider",width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=action).place(x=2,y=310)#creation boutton
    contenu.place(x=-1,y=-1)

def fonc(liste):
    fenPrincipale.geometry("900x500")
    new_frame()
    global contenu
    contenu.configure(width=901,height=501)
    global numero_fen
    image = Image.open("./images.png")
    resize_image = image.resize((901, 501))
    img = ImageTk.PhotoImage(resize_image)
    a = Label(contenu, image=img)
    a.image = img
    listebut=[]
    a.place(x=-1,y=-1)
    fenPrincipale.title("Interface caisier")
    scframe=Frame(contenu,height=300,width=1) # la frame qui affiche les produits sont stockés avec leur images
    scframe2=Frame(contenu,height=500,width=1) #la frame qui affiche panier
    catego=StringVar(value="Fruits et Légumes")
    Label(contenu,textvariable=catego,bg='black',fg='white',font=("Courier", 20, "italic","bold")).place(x=120,y=20)
    def cree(text,text3,text4,text5):
        liste_cat=["fruits et legumes","boulangerie","boucherie et poissonnerie","entretien"]
        for i in database.execute("SELECT NAME,IMAGE,ID FROM article WHERE CATEGORIE='%s'"% liste_cat[0]):
            image = Image.open(i[1])
            resize_image = image.resize((100, 100))
            img = ImageTk.PhotoImage(resize_image)
            button1 = Button(text, image=img,command = lambda a=i[0]:info(a))
            button1.image = img
            text.window_create("end", window=button1)
            text.insert("end", "    "+i[0]+"\t")
            text.window_create("end", window=listebut[i[2]-1])
            text.insert("end", "\n")
        for i in database.execute("SELECT NAME,IMAGE,ID FROM article WHERE CATEGORIE='%s'"% liste_cat[1]):
            image = Image.open(i[1])
            resize_image = image.resize((100, 100))
            img = ImageTk.PhotoImage(resize_image)
            button1 = Button(text3, image=img,command = lambda a=i[0]:info(a))
            button1.image = img
            text3.window_create("end", window=button1)
            text3.insert("end", "    "+i[0]+"\t")
            text3.window_create("end", window=listebut[i[2]-1])
            text3.insert("end", "\n")
        for i in database.execute("SELECT NAME,IMAGE,ID FROM article WHERE CATEGORIE='%s'"% liste_cat[2]):
            image = Image.open(i[1])
            resize_image = image.resize((100, 100))
            img = ImageTk.PhotoImage(resize_image)
            button1 = Button(text4, image=img,command = lambda a=i[0]:info(a))
            button1.image = img
            text4.window_create("end", window=button1)
            text4.insert("end", "    "+i[0]+"\t")
            text4.window_create("end", window=listebut[i[2]-1])
            text4.insert("end", "\n")
        for i in database.execute("SELECT NAME,IMAGE,ID FROM article WHERE CATEGORIE='%s'"% liste_cat[3]):
            image = Image.open(i[1])
            resize_image = image.resize((100, 100))
            img = ImageTk.PhotoImage(resize_image)
            button1 = Button(text5, image=img,command = lambda a=i[0]:info(a))
            button1.image = img
            text5.window_create("end", window=button1)
            text5.insert("end", "    "+i[0]+"\t")
            text5.window_create("end", window=listebut[i[2]-1])
            text5.insert("end", "\n")
        text.config(state='disabled')
        text3.config(state='disabled')
        text4.config(state='disabled')
        text5.config(state='disabled')
    text = Text(scframe,height=13,width=35,font=("Courier", 15, "italic","bold"))
    text.pack(side = LEFT,fill=BOTH)
    text3 = Text(scframe,height=13,width=35,font=("Courier", 15, "italic","bold"))
    text4 = Text(scframe,height=13,width=35,font=("Courier", 15, "italic","bold"))
    text5 = Text(scframe,height=13,width=35,font=("Courier", 15, "italic","bold"))
    scroll = Scrollbar(scframe,width=15,orient=VERTICAL)
    text.config(yscrollcommand=scroll.set)
    for i in database.execute("SELECT NAME,STOCK,CATEGORIE FROM article"):
        if i[2]=="fruits et legumes":
            a=text
        if i[2]=="boulangerie":
            a=text3
        if i[2]=="boucherie et poissonnerie":
            a=text4
        if i[2]=="entretien":
            a=text5
        button = Button(a, text="add")
        button.config(command = lambda a=i[0],b=button:add(a,b,tot))
        if i[1]==0:
            button.config(state='disabled')
        listebut.append(button)
    cree(text,text3,text4,text5)
    scroll.pack(side = RIGHT,fill=BOTH)
    Label(contenu,text="Panier",bg='black',fg='white',font=("Courier", 20, "italic","bold")).place(x=620,y=20)
    text2 = Text(scframe2,height=18,width=50,font=("Arial", 10, "italic","bold"))
    text2.insert("end","ID"+"\t"+"NOM"+"\t"+"PRIX"+"\t"+"QUANT"+"\t"+"TOTAL"+"\n")
    text2.pack(side = LEFT,fill=BOTH)
    scroll2 = Scrollbar(scframe2,width=15,orient=VERTICAL)
    text2.config(yscrollcommand=scroll2.set)
    scroll2.pack(side = RIGHT,fill=BOTH)
    tot=DoubleVar(0.0)
    total=0
    Label(contenu,text="Total:",font=("Arial", 20, "italic","bold")).place(x=580,y=420)
    Label(contenu,textvariable=tot,font=("Arial", 20, "italic","bold")).place(x=580,y=455)
    def info(var):
        fen = Toplevel()  # cree une fenetre
        fen.grab_set()
        fen.title("Info "+ var)  # titre de la fenetre
        fen.geometry("600x400")  # taille de la fenetre
        fen.resizable(False, False) 
        fen.configure(bg='white')#couleur background window
        cb=Frame(fen)
        cb.configure(width=601,height=401)
        image = Image.open("./images.png")
        resize_image = image.resize((601, 401))
        img = ImageTk.PhotoImage(resize_image)
        ab = Label(cb, image=img)
        ab.image = img
        ab.place(x=-1,y=-1)
        Label(cb,text="Info",bg='black',fg='white',font=("Courier", 30, "italic","bold")).place(x=250,y=10)
        def ret():
            fen.grab_release()
            fen.destroy()
        for i in database.execute("SELECT IMAGE FROM article where NAME='%s'"% var):
            image = Image.open(i[0])
            resize_image = image.resize((100, 100))
            img = ImageTk.PhotoImage(resize_image)
            ab = Label(cb, image=img)
            ab.image = img
            ab.place(x=70,y=80)
        for i in database.execute("SELECT NAME,PRICE,ID,CATEGORIE,STOCK FROM article where NAME='%s'"% var):
            Label(cb, text = "name:"+str(i[0]),bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=250, y=120)
            Label(cb, text = "price:"+str(i[1]),bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=420, y=120)
            Label(cb, text = "id:"+str(i[2]),bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=70, y=240)
            Label(cb, text = "categorie:\n"+str(i[3]),bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=200, y=240)
            Label(cb, text = "stock:"+str(i[4]),bg='black',fg='white',font=("Courier", 15, "italic","bold")).place(x=450, y=240)
        Button(cb, text="exit",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=ret).place(x=220,y=335)
        cb.place(x=-1,y=-1)
    def delt(var,but,tot):
        total=0
        text2.configure(state='normal')
        count=0
        for i in liste:
            if i[0]==var:
                i[1]=i[1]-1
                if i[1]<=0:
                    del liste[count]
            count=count+1
        text2.delete('1.0', END)
        text2.insert("end","ID"+"\t"+"NOM"+"\t"+"PRIX"+"\t"+"QUANT"+"\t"+"TOTAL")
        for r in liste:
            for i in database.execute("SELECT ID,NAME,PRICE FROM article WHERE NAME='%s'"% r[0]):
                total=round((total+(r[1]*i[2])),2)
                text2.insert("end", "\n"+str(i[0])+"\t"+str(i[1])+"\t"+str(i[2])+"\t"+str(r[1])+"\t"+str(round((r[1]*i[2]),2))+"\t")
                button3 = Button(text2, text="sup")
                button3.config(command = lambda a=i[1],b=but:delt(a,b,tot))
                text2.window_create("end", window=button3)
        text2.configure(state='disabled')
        
        if len(liste)==0:
            total=0.0
        tot.set(total)
        for i in liste:
            if var==i[0]:
                for r in database.execute("SELECT STOCK,ID FROM article WHERE NAME='%s'"% i[0]):
                    if not i[1]==r[0]:
                        listebut[r[1]-1].config(state= 'normal')
    def add(var,but,tot):
        total=0
        text2.configure(state='normal')
        addition=False
        for i in liste:
            if var==i[0]:
                i[1]=i[1]+1
                addition=True
        if not addition:
            liste.append([var,1])
        text2.delete('1.0', END)
        text2.insert("end","ID"+"\t"+"NOM"+"\t"+"PRIX"+"\t"+"QUANT"+"\t"+"TOTAL")
        for r in liste:
            for i in database.execute("SELECT ID,NAME,PRICE FROM article WHERE NAME='%s'"% r[0]):
                total=round((total+(r[1]*i[2])),2)
                text2.insert("end", "\n"+str(i[0])+"\t"+str(i[1])+"\t"+str(i[2])+"\t"+str(r[1])+"\t"+str(round((r[1]*i[2]),2))+"\t")
                button3 = Button(text2, text="sup")
                button3.config(command = lambda a=i[1],b=but:delt(a,b,tot))
                text2.window_create("end", window=button3)
        text2.configure(state='disabled')
        tot.set(total)
        for i in liste:
            if var==i[0]:
                for r in database.execute("SELECT STOCK,ID FROM article WHERE NAME='%s'"% i[0]):
                    if i[1]==r[0]:
                        print(r[1])
                        listebut[r[1]-1].config(state= DISABLED)
    pag=IntVar(value=1)
    liste2=liste
    liste=[]
    for r in liste2:
        for i in range(1,r[1]+1):
            for d in database.execute("SELECT ID FROM article WHERE NAME='%s'"% r[0]):
                add(r[0],listebut[d[0]-1],tot)
    scroll.config(command=text.yview)
    text2.configure(state='disabled')
    scroll2.config(command=text2.yview)
    scframe.place(x=20,y=110)
    scframe2.place(x=500,y=110)
    def pay():
        if not len(liste)==0:
            resultat(liste,tot.get())
    global status
    if status=="manager":
        fenbtn = Button(contenu, text="Return",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=manage).place(x=380,y=425)#creation button
    if status=="caisier":
        fenbtn = Button(contenu, text="Log out",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=login).place(x=380,y=425)#creation button
    def pag_pre(text):
        if pag.get()==2:
            buut1.config(state='disabled')
        elif pag.get()==4:
            buut2.config(state='normal')
        pag.set(pag.get()-1)
        if pag.get()==1:
            text3.pack_forget()
            text.pack(side = LEFT,fill=BOTH)
            text.config(yscrollcommand=scroll.set)
            scroll.config(command=text.yview)
            catego.set(value="Fruits et Légumes")
        if pag.get()==2:
            text4.pack_forget()
            text3.pack(side = LEFT,fill=BOTH)
            text3.config(yscrollcommand=scroll.set)
            scroll.config(command=text3.yview)
            catego.set(value="Boulangerie")
        if pag.get()==3:
            text5.pack_forget()
            text4.pack(side = LEFT,fill=BOTH)
            text4.config(yscrollcommand=scroll.set)
            scroll.config(command=text4.yview)
            catego.set(value="Boucherie et Poissonnerie")

    def pag_next():
        if pag.get()==1:
            buut1.config(state='normal')
        elif pag.get()==3:
            buut2.config(state='disabled')
        pag.set(pag.get()+1)
        if pag.get()==2:
            text.pack_forget()
            text3.pack(side = LEFT,fill=BOTH)
            text3.config(yscrollcommand=scroll.set)
            scroll.config(command=text3.yview)
            catego.set(value="Boulangerie")
        if pag.get()==3:
            text3.pack_forget()
            text4.pack(side = LEFT,fill=BOTH)
            text4.config(yscrollcommand=scroll.set)
            scroll.config(command=text4.yview)
            catego.set(value="Boucherie et Poissonnerie")
        if pag.get()==4:
            text4.pack_forget()
            text5.pack(side = LEFT,fill=BOTH)
            text5.config(yscrollcommand=scroll.set)
            scroll.config(command=text5.yview)
            catego.set(value="Produits d'entretien")

    Label(contenu,textvariable=pag,font=("Arial", 20, "italic","bold")).place(x=175,y=440)
    Label(contenu,text="/4",font=("Arial", 20, "italic","bold")).place(x=195,y=440)
    buut2=Button(contenu, text=">",height=1,width=3,fg='white',bg='black',font=("Courier", 20, "italic"), command=pag_next)
    buut2.place(x=260,y=430)
    buut1=Button(contenu, text="<",height=1,width=3,fg='white',bg='black',font=("Courier", 20, "italic"),state='disabled', command=lambda a=text:pag_pre(a))
    buut1.place(x=80,y=430)
    Button(contenu, text="Payer",height=1,width=8,fg='white',bg='black',font=("Courier", 20, "italic"), command=pay).place(x=725,y=425)
    contenu.place(x=-1,y=-1)

def suivi():# affichage graphe en usant Matplolib
    fenPrincipale.geometry("800x600")
    new_frame()
    contenu.configure(width=801,height=601)
    global numero_fen
    image = Image.open("./images.png")
    resize_image = image.resize((801, 601))
    img = ImageTk.PhotoImage(resize_image)
    a = Label(contenu, image=img)
    a.image = img
    a.place(x=-1,y=-1)
    fenPrincipale.title("suivi vente")  # titre de la fenetre
    fig = Figure()
    fig.set_size_inches(8, 5.56, forward=True)
    liste=[]
    liste2=[]
    count=0
    for i in database.execute("SELECT TOTAL FROM vente"): # liste avec total des ventes
        liste.append(int(i[0]))
    for i in liste: # creation d'un range avec toutes les variables
        for r in range(0,i):
            liste2.append(count)
        count=count+1
    fig.add_subplot(111).hist(tuple(liste2), range=(0, 7), bins=7,facecolor='blue',alpha=0.5)
    canvas = FigureCanvasTkAgg(fig, master=contenu)  # creation histogramme
    canvas.draw()#insertion de l'histogramme
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)#insertion de la fenetre de l'histogramme dans le tkinter
    x=0
    for i in database.execute("SELECT TOTAL FROM vente"):#affichage total des vente pour chaque jour
        for r in i:
            Label(contenu,text=str(r)).place(x=150+x,y=520)
            x=x+80
    fenbtn = Button(contenu, text="Return",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=manage).pack(side=TOP)
    contenu.place(x=-1,y=-1)

def ajout():# creation d'interface d'ajout d'un utilisateur
    fenPrincipale.geometry("800x800")
    new_frame()
    contenu.configure(width=801,height=801)
    global numero_fen
    image = Image.open("./images.png")
    resize_image = image.resize((801, 801))
    img = ImageTk.PhotoImage(resize_image)
    a = Label(contenu, image=img)
    a.image = img
    a.place(x=-1,y=-1)
    global numero_fen
    numero_fen=2
    fenPrincipale.title("Ajout caisier")  # titre de la fenetre

    iden = StringVar()
    nom = StringVar()
    prenom = StringVar()
    date= StringVar()
    add = StringVar()
    code= StringVar()
    login = StringVar()
    mdep= StringVar()

    Label(contenu,text="Add seller",bg='black',fg='white',font=("Courier", 30, "italic","bold")).place(x=300,y=10)
    Label(contenu,text="Username",bg='black',fg='white',font=("Arial", 15, "italic","bold")).place(x=175,y=100)
    ids=Entry(contenu,textvariable=iden,width=20,bg='black',fg='white',font=("Comic sans ms", 20, "italic","bold"))#entree id
    ids.place(x=300,y=100)
    Label(contenu,text="Name",bg='black',fg='white',font=("Arial", 15, "italic","bold")).place(x=175,y=175)
    name = Entry(contenu,textvariable=nom,width=20,bg='black',fg='white',font=("Comic sans ms", 20, "italic","bold"))#entree nom
    name.place(x=300,y=175)
    Label(contenu,text="First name",bg='black',fg='white',font=("Arial", 15, "italic","bold")).place(x=175,y=250)
    lastname=Entry(contenu,textvariable=prenom,width=20,bg='black',fg='white',font=("Comic sans ms", 20, "italic","bold"))#entree prenom
    lastname.place(x=300,y=250)
    Label(contenu,text="Date of birth",bg='black',fg='white',font=("Arial", 15, "italic","bold")).place(x=150,y=315)
    Label(contenu,text="(YYYY/MM/DD)",bg='black',fg='white',font=("Courier", 13, "italic")).place(x=150,y=350)
    dat = Entry(contenu,textvariable=date,width=20,bg='black',fg='white',font=("Comic sans ms", 20, "italic","bold"))#entree date de naissance
    dat.place(x=300,y=325)
    Label(contenu,text="Address",bg='black',fg='white',font=("Arial", 15, "italic","bold")).place(x=175,y=400)
    addresse = Entry(contenu,textvariable=add,width=20,bg='black',fg='white',font=("Comic sans ms", 20, "italic","bold"))#entree addresse
    addresse.place(x=300,y=400)
    Label(contenu,text="Post code",bg='black',fg='white',font=("Arial", 15, "italic","bold")).place(x=175,y=475)
    code = Entry(contenu,textvariable=code,width=20,bg='black',fg='white',font=("Comic sans ms", 20, "italic","bold"))#entree code postal
    code.place(x=300,y=475)
    Label(contenu,text="Login",bg='black',fg='white',font=("Arial", 15, "italic","bold")).place(x=150,y=540)
    Label(contenu,text="(letter and number only)",bg='black',fg='white',font=("Courier", 13, "italic")).place(x=50,y=575)
    log = Entry(contenu,textvariable=login,width=20,bg='black',fg='white',font=("Comic sans ms", 20, "italic","bold"))#entree login
    log.place(x=300,y=550)
    Label(contenu,text="Password",bg='black',fg='white',font=("Arial", 15, "italic","bold")).place(x=100,y=625)
    Label(contenu,text="(with uppercase,lowercase\n,special character)",bg='black',fg='white',font=("Courier", 13, "italic")).place(x=20,y=660)
    mdp = Entry(contenu,textvariable=mdep,width=20,bg='black',fg='white',font=("Comic sans ms", 20, "italic","bold"))#entree mot de passe
    mdp.place(x=300,y=625)

    def vider():#vider le contenu des entree
        ids.delete(0,"end")
        name.delete(0,"end")
        lastname.delete(0,"end")
        dat.delete(0,"end")
        addresse.delete(0,"end")
        code.delete(0,"end")
        log.delete(0,"end")
        mdp.delete(0,"end")

    def register():#fonction verification des entree et ajout dans la base de donnee
        if len(ids.get())==0:
            messagebox.showwarning("Error","The username entry is empty")
            return
        if len(name.get())==0:
            messagebox.showinfo("add seller","the seller sucessfuly add")
        if len(dat.get())==0:
            messagebox.showwarning("Error","The date entry is empty")
            return
        if len(addresse.get())==0:
            messagebox.showwarning("Error","The address entry is empty")
            return
        if len(code.get())==0:
            messagebox.showwarning("Error","The post code entry is empty")
            return
        if len(log.get())==0:
            messagebox.showwarning("Error","The login entry is empty")
            return
        if len(mdp.get())==0:
            messagebox.showwarning("Error","The password entry is empty")
            return
        if len(dat.get())!=10:
            messagebox.showwarning("Error","The date entry have not the good lenght")
            return
        if len(code.get())!=5:
            messagebox.showwarning("Error","The post code entry have not the good lenght")
            return
        if len(mdp.get())<8:
            messagebox.showwarning("Error","the length of the password is not respected")
            return
        valid_username=True
        for i in database.execute("SELECT * FROM liste WHERE ID = '%s'"% ids.get()):
            valid_username=False
        if not valid_username:
            messagebox.showwarning("Error","The username already exists")
            return
        liste=dat.get()
        if not liste[0:4].isnumeric() and not liste[5:7].isnumeric() and not liste[8:10].isnumeric():
            messagebox.showwarning("Error","The date must have only numbers and /")
            return
        if int(liste[5:7])<=0 or int(liste[5:7])>12:
            messagebox.showwarning("Error","This month doesn't exist")
            return
        if int(liste[8:10])<=0 or int(liste[8:10])>31:
            messagebox.showwarning("Error","This day doesn't exist")
            return
        if liste[4]!='/' and liste[7]!='/':
            messagebox.showwarning("Error","Put only / between the year and month and between month and day")
            return
        if not code.get().isnumeric():
            messagebox.showwarning("Error","The post code must have only numbers")
            return
        if not log.get().isalnum():
            messagebox.showwarning("Error","the login does not only have numbers and letters")
            return
        valid_login=True
        for i in database.execute("SELECT * FROM liste WHERE LOGIN = '%s'"% log.get()):
            valid_login=False
        if not valid_login:
            messagebox.showwarning("Error","The login already exists")
            return
        maj=False
        mini=False
        carac=False
        for i in mdp.get():
            if i.isupper():
                maj=True
            if i.islower():
                mini=True
            if not i.isalnum():
                carac=True
        if not maj:
            messagebox.showwarning("Error","the password does not have a capital letter")
            return
        if not mini:
            messagebox.showwarning("Error","the password has no lowercase")
            return
        if not carac:
            messagebox.showwarning("Error","the password has no special character")
            return
        database.execute("INSERT INTO liste VALUES (?,?,?,?,?,?,?,?,?)",(ids.get(),name.get(),lastname.get(),dat.get(),addresse.get(),int(code.get()),log.get(),mdp.get(),"caisier"))
        base.commit()
        messagebox.showinfo("add seller","the seller sucessfuly add")
        manage()

    fenbtn = Button(contenu, text="Register",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=register).place(x=50,y=725)#creation button
    fenbtn = Button(contenu, text="Clear",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=vider).place(x=300,y=725)#creation button
    fenbtn = Button(contenu, text="Return",height=1,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=manage).place(x=550,y=725)#creation button
    contenu.place(x=-1,y=-1)

def login():#creation interface de connexion
    fenPrincipale.geometry("800x400")
    new_frame()
    global contenu
    contenu.configure(width=801,height=401)
    global numero_fen
    image = Image.open("./images.png")
    resize_image = image.resize((801, 401))
    img = ImageTk.PhotoImage(resize_image)
    a = Label(contenu, image=img)
    a.image = img
    a.place(x=-1,y=-1)
    numero_fen=0
    md = StringVar()
    user = StringVar()
    def entree(_event):
        global numero_fen
        if numero_fen==0:
            verife()

    def verife():#fonction verification des entree
        print("verification...")
        if len(user.get())==0:
            messagebox.showwarning("Error","The login entry is empty")
            return
        if len(md.get())==0:
            messagebox.showwarning("Error","The password entry is empty")
            return
        if len(md.get())<8:
            messagebox.showwarning("Error","the length of the password is not respected")
            return
        if not user.get().isalnum():
            messagebox.showwarning("Error","the login does not only have numbers and letters")
            return
        maj=False
        mini=False
        carac=False
        for i in md.get():
            if i.isupper():
                maj=True
            if i.islower():
                mini=True
            if not i.isalnum():
                carac=True
        if not maj:
            messagebox.showwarning("Error","the password does not have a capital letter")
            return
        if not mini:
            messagebox.showwarning("Error","the password has no lowercase")
            return
        if not carac:
            messagebox.showwarning("Error","the password has no special character")
            return
        existe=False
        liste=()
        for i in database.execute("SELECT * FROM liste WHERE LOGIN = ? AND PASSWORD = ?",(user.get(), md.get())):
            liste=i
            existe=True
        if existe:
            global status
            if liste[8]=='manager':
                print("reusis")

                status=liste[8]
                manage()
            if liste[8]=='caisier':
                print("reusis")
                status=liste[8]
                fonc([])
        else:
            messagebox.showwarning("Error","login or password invalid")
            return
    
    Label(contenu,text="Login",bg='black',fg='white',font=("Courier", 30, "italic","bold")).place(x=325,y=10)
    Label(contenu,text="Username",bg='black',fg='white',font=("Arial", 15, "italic","bold")).place(x=190,y=103)
    entr =Entry(contenu,textvariable=user,width=20,bg='black',fg='white',font=("Comic sans ms", 20, "italic","bold"))#entree login
    entr.place(x=300,y=100)
    Label(contenu,text="(ne peut contenir que des lettre et des chiffre)",bg='black',fg='white',font=("Courier", 13, "italic")).place(x=150,y=145)

    Label(contenu,text="Password",bg='black',fg='white',font=("Arial", 15, "italic","bold")).place(x=190,y=203)
    ent=Entry(contenu,textvariable=md,show="*",width=20,bg='black',fg='white',font=("Comic sans ms", 20, "italic","bold"))#entree mot de passe
    ent.place(x=300,y=200)
    Label(contenu,text="(doit contenir 1 lettre maj, 1 lettre min, 1 caractére spec)",bg='black',fg='white',font=("Courier", 13, "italic")).place(x=80,y=245)

    Button(contenu, text="Connexion",height=2,fg='white',bg='black',font=("Courier", 20, "italic"), command=verife).place(x=100,y=300)#creation boutton
    Button(contenu, text="Exit",height=2,width=10,fg='white',bg='black',font=("Courier", 20, "italic"), command=fenPrincipale.destroy).place(x=525,y=300)#creation boutton
    entr.bind('<Return>', entree)
    ent.bind('<Return>', entree)
    contenu.place(x=-1,y=-1)

login()
fenPrincipale.mainloop()#affichage window
