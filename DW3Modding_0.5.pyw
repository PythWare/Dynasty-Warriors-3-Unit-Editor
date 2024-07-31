import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import shutil
file1 = "DW3.iso"
unit_data = [15, 404]# chunk that is 15 long for unit data and total amount of unit slots which is 404
backup = "backups_for_mod_disabling"
data_storage = "DW3UnitData"
icon_fold = "Icon_Files"
unit_file = "Unit.DW3Data"
unit_ref = "Unit.DW3Ref"
dw3_ext = ".DW3UnitMod"
class CheckIt:
    @staticmethod
    def validate_numeric_input(new_value):
        return new_value == "" or (new_value.replace(".", "", 1).isdigit() and '.' not in new_value and float(new_value) >= 0)
def rem(files1, files2): # everytime the script is ran delete the old files to create fresh unmodified versions
    filepath1 = os.path.join(data_storage, files1)
    if os.path.isfile(filepath1):
            os.remove(filepath1)
    filepath2 = os.path.join(data_storage, files2)
    if os.path.isfile(filepath2):
        os.remove(filepath2)
class UnitEditor(CheckIt):
    def __init__(self, root):
        self.root = root
        self.root.title("Dynasty Warriors 3 Unit Editor")
        self.root.iconbitmap(os.path.join(icon_fold, "img2.ico"))
        self.root.minsize(800,800)
        self.root.resizable(False,False)

        self.unit_path = os.path.join(data_storage, unit_file)
        self.bunit_path = os.path.join(backup, unit_file)
        self.unit_ref_data = os.path.join(data_storage, unit_ref)
        self.unit_reading()
        self.unit_ref()

        self.mod_manager = tk.Button(self.root, text = "DW3 Mod Manager", command = self.open_mod_manager, height = 10)
        self.mod_manager.place(x=30, y=600)
        self.cred = tk.Label(self.root, text = "Credit goes to Michael for DW3 unit_data documentation.")
        self.cred.place(x=180, y=700)
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.place(x=480, y=200)  # For displaying if a non-integer value was used in an entry or issue creating a mod
        # Registering validate_numeric_input for validation
        validate_cmd = (self.root.register(CheckIt.validate_numeric_input), "%P")
        
        self.name = tk.IntVar() # 2 bytes
        self.modelmotion = tk.IntVar()
        self.color = tk.IntVar()
        self.moveset = tk.IntVar()
        self.horse = tk.IntVar()
        self.bowattack = tk.IntVar()
        self.bowdefense = tk.IntVar()
        self.mountedattack = tk.IntVar()
        self.mounteddefense = tk.IntVar()
        self.speed = tk.IntVar()
        self.guardspeed = tk.IntVar()
        self.jumpheight = tk.IntVar()
        self.weapon = tk.IntVar()
        self.itemcount = tk.IntVar()
        self.modname = tk.StringVar()
        hex_values = [hex(i) for i in range(unit_data[1])]
        
        self.labels = ["Name", "Model/Motion", "Color", "Moveset", "Horse", "Bow Attack", "Bow Defense",
               "Mounted Attack", "Mounted Defense", "Speed", "Guard Speed", "Jump height", "Weapon",
               "Item Amount"]
        
        self.entry_vars = [self.name, self.modelmotion, self.color, self.moveset, self.horse, self.bowattack,
                           self.bowdefense, self.mountedattack, self.mounteddefense, self.speed, self.guardspeed, self.jumpheight,
                           self.weapon, self.itemcount]
        
        for i, (label_text, entry_var) in enumerate(zip(self.labels, self.entry_vars)):
            y_position = i * 40
            tk.Label(self.root, text=label_text).place(x=160, y=y_position)
            tk.Entry(self.root, textvariable=entry_var, validate="key",
                     validatecommand=validate_cmd).place(x=0, y=y_position)

        self.selected_slot = tk.IntVar(self.root)
        self.selected_slot.set(0)  # Default value
        slot_combobox = ttk.Combobox(self.root, textvariable=self.selected_slot, values=hex_values)
        slot_combobox.bind("<<ComboboxSelected>>", self.slot_selected)
        slot_combobox.place(x=600, y=10)

        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.place(x=480, y=200)  # For displaying if a non-integer value was used in an entry or issue creating a mod

        tk.Button(self.root, text="Submit values to .DW3Data file", command= self.submit_unit, height=5).place(x=600, y=250)
        tk.Button(self.root, text = "Create Unit Mod", command = self.create_unit_mod, height=5, width=20).place(x=600,y=450)
        mm1 = tk.Entry(self.root, textvariable = self.modname).place(x=600,y=400)
        mm2 = tk.Label(self.root, text = f"Enter a mod name").place(x=490,y=400)

    # Function to handle selection change
    def on_select(self, event):
        selected_unit = self.combo.get()

    def slot_selected(self, event=None): # update display data
        self.selected_slot_value = self.selected_slot.get()
        self.unit_display(self.selected_slot_value)
    def submit_unit(self):
        try:
            col = [self.name.get().to_bytes(2, "little"), self.modelmotion.get().to_bytes(1, "little"), self.color.get().to_bytes(1, "little"),
                         self.moveset.get().to_bytes(1, "little"), self.horse.get().to_bytes(1, "little"), self.bowattack.get().to_bytes(1, "little"),
                         self.bowdefense.get().to_bytes(1, "little"), self.mountedattack.get().to_bytes(1, "little"), self.mounteddefense.get().to_bytes(1, "little"),
                         self.speed.get().to_bytes(1, "little"), self.guardspeed.get().to_bytes(1, "little"), self.jumpheight.get().to_bytes(1, "little"),
                         self.weapon.get().to_bytes(1, "little"), self.itemcount.get().to_bytes(1, "little")]
            unit_slot = self.selected_slot.get()
            with open(self.unit_ref_data, "rb") as r1: # for obtaining the offset for a unit slot from the .ref file
                uservalue = unit_slot * 8
                r1.seek(uservalue)
                getoffset = int.from_bytes(r1.read(8), "little")
                with open(self.unit_path, "r+b") as f1: # for updating the unit slot with the current values from collectit
                    f1.seek(getoffset)
                    for b in col:
                        f1.write(b)                       
            self.status_label.config(text=f"Values submitted successfully.", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg="red")
        
    def create_unit_mod(self): # for creating a mod file with custom extension
        global getoffset
        sep = "." # to be used for correcting possible user filenames that have their own extension
        try:
            usermodname = self.modname.get().split(sep, 1)[0] + dw3_ext # Create modname with the user entered name and stage extension based on the .ref file selected
            with open(self.unit_path, "rb") as r1:
                data = r1.read()
                offset = r1.tell()
                with open(usermodname, "wb") as w1:
                    w1.write(data)
            self.status_label.config(text=f"Mod file '{usermodname}' created successfully.", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error creating mod file '{usermodname}': {str(e)}", fg="red")

    def unit_reading(self):
        global getoffset
        aob_pattern = b'\x07\x06\x06\x05\x05\x04\x04\x03\x03\x02\x02\x02\x02\x01\x00\x00'
        chunk_size = 4096  # Adjust chunk size as needed, depending on your system's memory and performance
        with open(file1, "rb") as f1:
            offset = 0
            found = False
            
            while not found:
                chunk = f1.read(chunk_size)
                if not chunk:
                    break  # End of file
                
                # Search for the pattern in the current chunk
                pattern_offset = chunk.find(aob_pattern)
                
                if pattern_offset != -1:
                    # Calculate the absolute offset in the ISO file
                    getoffset = offset + pattern_offset + 16
                    
                    with open(self.unit_path, "ab") as f2:
                        # Seek to the calculated offset in the ISO file
                        f1.seek(getoffset)
                        
                        # Read and write the data to self.unit_path
                        for i in range(unit_data[1]):
                            unitdata1 = f1.read(unit_data[0])
                            f2.write(unitdata1)
                        f2.write(getoffset.to_bytes(4, "little"))
                    found = True  # Exit loop since pattern is found
                
                offset += chunk_size
        
        if not found:
            print("AOB pattern not found in ISO file.")

        if not os.path.exists(self.bunit_path):
            shutil.copy(self.unit_path, self.bunit_path)
    def unit_ref(self):
        with open(self.unit_path, "rb") as r1:  # Open the corresponding .ref file for writing
            with open(self.unit_ref_data, "ab") as r2:
                offset = 0  # Initialize offset counter
                while True:
                    data_chunk = r1.read(unit_data[0])  # Read a 15-byte chunk from .data file
                    if not data_chunk:  # Break loop if end of file is reached
                        break
                    r2.write(offset.to_bytes(8, "little"))  # Write the offset to the .ref file
                    offset += unit_data[0]  # Move offset to the next chunk
                    
    def unit_display(self, selected_slot_value):
        with open(self.unit_ref_data, "rb") as r1: # .ref file
            useroffset = self.selected_slot_value
            uservalue = self.selected_slot_value * 8
            r1.seek(uservalue)
            getoffset = int.from_bytes(r1.read(8), "little")
            with open(self.unit_path, "r+b") as r2:
                r2.seek(getoffset)
                unitname = int.from_bytes(r2.read(2), "little")
                unitmodelmotion = int.from_bytes(r2.read(1), "little")
                unitcolor = int.from_bytes(r2.read(1), "little")
                unitmoveset = int.from_bytes(r2.read(1), "little")
                unithorse = int.from_bytes(r2.read(1), "little")
                unitbowattack = int.from_bytes(r2.read(1), "little")
                unitbowdefense = int.from_bytes(r2.read(1), "little")
                unitmountedattack = int.from_bytes(r2.read(1), "little")
                unitmounteddefense = int.from_bytes(r2.read(1), "little")
                unitspeed = int.from_bytes(r2.read(1), "little")
                unitguardspeed = int.from_bytes(r2.read(1), "little")
                unitjumpheight = int.from_bytes(r2.read(1), "little")
                unitweapon = int.from_bytes(r2.read(1), "little")
                unititemcount = int.from_bytes(r2.read(1), "little")

                self.name.set(unitname)
                self.modelmotion.set(unitmodelmotion)
                self.color.set(unitcolor)
                self.moveset.set(unitmoveset)
                self.horse.set(unithorse)
                self.bowattack.set(unitbowattack)
                self.bowdefense.set(unitbowdefense)
                self.mountedattack.set(unitmountedattack)
                self.mounteddefense.set(unitmounteddefense)
                self.speed.set(unitspeed)
                self.guardspeed.set(unitguardspeed)
                self.jumpheight.set(unitjumpheight)
                self.weapon.set(unitweapon)
                self.itemcount.set(unititemcount)
    def open_mod_manager(self):
        manager = DW3Manager(self.root)
        
class DW3Manager: # mod manager for unit mods
    def __init__(self, root):
        self.root = tk.Toplevel()
        self.root.title("DW3 Mod Manager")
        self.root.iconbitmap(os.path.join(icon_fold, "img1.ico"))
        self.root.minsize(400, 400)
        self.root.resizable(False, False)
        self.mod_status = tk.Label(self.root, text="", fg="green")
        self.mod_status.place(x=10, y=170)
        tk.Button(self.root, text="Enable Mod", command=self.ask_open_file, height=10, width=50).place(x=10, y=10) # button for enabling mods
        tk.Button(self.root, text="Disable Mod", command=self.ask_open_ofile, height=10, width=50).place(x=10, y=210) # button for disabling mods
    def ask_open_file(self): # This is for enabling the user selected mod
        global getoffset
        file_path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select mod file",
            filetypes=(
                ("Supported Files", "*.DW3UnitMod;"),
            ))
        try:
            if file_path:
                offset = getoffset # offset for unit data in the iso file
                # Apply the mod to the iso file
                with open(file1, "r+b") as f1: # open iso file for reading and writing
                    with open(file_path, "rb") as f2: # open the mod file for reading
                        f1.seek(offset) # seek the offset in the iso file
                        sdata = f2.read(19690) # read the mod file's data
                        f1.write(sdata) # write the mod file's data to the iso file
                self.mod_status.config(text=f"Mod file '{os.path.basename(file_path)}' enabled successfully.", fg="green")
        except Exception as e:
            self.mod_status.config(text=f"Error: {str(e)}", fg="red")
    def ask_open_ofile(self): # For disabling mods
        global getoffset
        file_path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select mod file",
            filetypes=(
                ("Supported Files", "*.DW3Data;"),
            ))
        try:
            if file_path:
                offset = getoffset # offset for unit data in the iso file
                # apply the mod disabling file to the iso file
                with open(file1, "r+b") as f1: # open the iso file for reading and writing
                    with open(file_path, "rb") as f2: # open the mod disabling file
                        f1.seek(offset) # seek offset for unit data in the iso file
                        sdata = f2.read(19690) # read the data for disabling unit mods
                        f1.write(sdata) # write the data
                self.mod_status.config(text=f"The mod that used the '{os.path.basename(file_path)}' template was disabled.", fg="green")
        except Exception as e:
            self.mod_status.config(text=f"Error: {str(e)}", fg="red")
def main():
    root = tk.Tk()
    dw3u = UnitEditor(root)
    root.mainloop()
if __name__ == "__main__":
    os.makedirs(backup, exist_ok = True)
    os.makedirs(data_storage, exist_ok = True)
    os.makedirs(icon_fold, exist_ok = True)
    rem(unit_file, unit_ref)
    main()
