import sys
import pickle
import os

if sys.version_info < (3, 0):
	# Python 2
	import Tkinter as tk
else:
	# Python 3
	import tkinter as tk

class App:
	def __init__(self, master):
		# frame = tk.Frame(master)
		# frame.pack()

		# try/except
		try:
			with open('siteslist', 'rb') as data:
				self.sites = pickle.load(data)
		except:
			self.sites = []

		self.add = tk.Button(master, text="Add Site", command=self.add_site)
		self.add.grid(row=0, column=1)

		self.remove = tk.Button(master, text="Remove Site", command=self.remove_site)
		self.remove.grid(row=1, column=1)

		self.enter = tk.Entry(master)
		self.enter.grid(row=0, column=0)

		self.listbox = tk.Listbox(master)
		self.listbox.grid(row=1, column=0)
		for item in self.sites:
			self.listbox.insert("end", item)

		self.block = tk.Button(master, text="Block Sites", command=self.block_sites)
		self.block.grid(row=2, column=1)

		self.unblock = tk.Button(master, text="Unblock Sites", command=self.unblock_sites)
		self.unblock.grid(row=3, column=1)

	def add_site(self):
		s = self.enter.get()
		self.listbox.insert("end", s)
		self.enter.delete(0, 'end')
		self.sites.append(s)
		update_siteslist(self)

	def remove_site(self):
		s = self.listbox.get("anchor")
		self.listbox.delete("anchor")
		self.sites.remove(s)
		update_siteslist(self)

	def block_sites(self):
		update_hosts(self)

	def unblock_sites(self):
		clear_hosts(self)

def update_hosts(self):
	command = """
	pw="$(osascript -e 'Tell application "System Events" to display dialog "Password:" default answer "" with hidden answer' -e 'text returned of result' 2>/dev/null)" && echo $pw | sudo -S echo "
# Host Database !
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1   localhost
255.255.255.255 broadcasthost
::1             localhost
fe80::1%lo0 localhost
"""
	for item in self.sites:
		command += "127.0.0.1 " + item + "\n"
	command += "\" | sudo tee /etc/hosts > /dev/null"

	os.system(command)

def clear_hosts(self):
	command = """
	pw="$(osascript -e 'Tell application "System Events" to display dialog "Password:" default answer "" with hidden answer' -e 'text returned of result' 2>/dev/null)" && echo $pw | sudo -S echo "
# Host Database !
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1   localhost
255.255.255.255 broadcasthost
::1             localhost
fe80::1%lo0 localhost
"""
	command += "\" | sudo tee /etc/hosts > /dev/null"
	os.system(command)

def update_siteslist(self):
	with open('siteslist', 'wb') as data:
		pickle.dump(self.sites, data)

root = tk.Tk()
root.title("Still")
app = App(root)
root.mainloop()


# root = tk.Tk()
# root.title("Sandwich")
# tk.Button(root, text="Add Site").pack()
# tk.Button(root, text="Remove Site").pack()
# tk.mainloop()
