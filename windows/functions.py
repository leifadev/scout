
def clearConsole_command(self):
        self.logfield["state"] = "normal"
        with open(self.ymldir, "r") as yml:
            data = yaml.load(yml, Loader=yaml.Loader)
            self.enablePrompts = data[0]['Options']['errorChoice']

        if self.enablePrompts:
            print("oooo")
            messagebox.showwarning("Warning", "Are you sure you want to clear the console?")
            self.logfield.delete("1.0","end")
        else:
            self.logfield.delete("1.0","end")
        self.logfield["state"] = "disabled"