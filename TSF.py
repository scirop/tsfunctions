#This piece of code can find the Greens Function Coefficients and Inverse Function Coefficients
#for a given vector of phi and theta.
#Created by: Swarup Sahoo (swarupsahoo@utexas.edu)
from tkinter import *
#import ctypes
#def Mbox(title, text, style):
#	ctypes.windll.user32.MessageBoxW(0, text, title, style)

def tsf(phi, theta):

	def showGreens():
		ArrLen=scale.get()
		greensArr.delete('1.0', END)
		if var1.get() == 1:
			for i in range(ArrLen):
				greensArr.insert(INSERT, "G%d:%s" % (i,round(funcTypes.ImpFindGreens(i, phi, theta),4)))
				greensArr.insert(END, "\n")
		else:
			greensArr.insert(INSERT, "Only works for ARMA(2,1) for now")
			greensArr.insert(END,"\n")
			for i in range(ArrLen):
				greensArr.insert(INSERT, "G%d:%s" % (i,round(funcTypes.ExpFindGreens(i, phi, theta),4)))
				greensArr.insert(END, "\n")

	def showInverses():
		ArrLen=scale.get()
		InversesArr.delete('1.0', END)
		if var1.get() == 1:
			for i in range(ArrLen):
				InversesArr.insert(INSERT,"I%d:%s" % (i,round(funcTypes.ImpFindInverses(i, phi, theta),4)))
				InversesArr.insert(END,"\n")
		else:
			InversesArr.insert(INSERT, "Only works for ARMA(2,1) for now")
			InversesArr.insert(END,"\n")
			for i in range(ArrLen):
				InversesArr.insert(INSERT,"I%d:%s" % (i,round(funcTypes.ExpFindInverses(i, phi, theta),4)))
				InversesArr.insert(END,"\n")

	n = len(phi)
	m = len(theta)	

	root = Tk()

	frame = Frame(root)
	frame.pack()


	var=IntVar()
	scaleLabel=Label(root, text="# of coefs:         ")
	scaleLabel.pack(anchor=NE)
	scale = Scale(root, variable = var, from_=1, to=11, orient=HORIZONTAL)
	scale.pack(anchor=NE)

	dispframe = Frame(root)
	dispframe.pack()

	root.iconbitmap('icon.ico')
	root.title("G.I.Joe")
	root.geometry('450x410+350+70')


	var1=IntVar()
	R1 = Radiobutton(root, text="Implicit", variable=var1, value=1)
	R1.pack( anchor = NW )
	R2 = Radiobutton(root, text="Explicit", variable=var1, value=2)
	R2.pack( anchor = NW )

	greensArr = Text(dispframe,  height= 11, width=20)
	greensArr.pack(side=LEFT)

	InversesArr = Text(dispframe, height= 11, width=20)
	InversesArr.pack(side=RIGHT)

	modelInfo = Text(frame, height=1, width=len("ARMA(%d,%d)" % (len(phi), len(theta))))
	modelInfo.insert(INSERT, "ARMA(%d,%d)" % (len(phi), len(theta)))
	modelInfo.pack()

	BG = Button(frame, text ="Greens", command = showGreens)
	BG.pack(side=LEFT)
	BI = Button(frame, text ="Inverses", command = showInverses)
	BI.pack(side=RIGHT)
	QuitButton = Button(root, text="Quit", command=root.quit)
	QuitButton.pack(side=BOTTOM)

	root.mainloop()



class funcTypes:

	def ImpFindGreens(num, phi, theta):
		G=0
		if num==0:
			G=1
		else:
			try:
				G=-theta[num-1]
			except IndexError:
				G=0

			for i in range(num):
				try:
					t=phi[i]
				except IndexError:
					phi.append(0)
				G+=phi[i]*funcTypes.ImpFindGreens(num-i-1, phi, theta)
		
		return G


	def ImpFindInverses(num, phi, theta):
		I = 0
		if num==0:
			I=-1
		else:
			try:
				I=phi[num-1]
			except IndexError:
				I=0

			for i in range(num):
				try:
					t=theta[i]
				except IndexError:
					theta.append(0)
				I+=theta[i]*funcTypes.ImpFindInverses(num-i-1, phi, theta)

		return I

	def ExpFindGreens(num, phi, theta):
		lam1=0.5*(phi[0]+(phi[0]**2+4*phi[1])**0.5)
		lam2=0.5*(phi[0]-(phi[0]**2+4*phi[1])**0.5)
		g1=(lam1-theta[0])/(lam1-lam2)
		g2=(lam2-theta[0])/(lam2-lam1)
		return (g1*lam1**num+g2*lam2**num).real

	def ExpFindInverses(num, phi, theta):
		if num==0:
			return -1
		elif num==1:
			return phi[0]-theta[0]
		else:
			return (phi[1]-theta[0]*(theta[0]-phi[0]))*theta[0]**(num-2)