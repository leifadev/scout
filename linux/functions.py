
def clearConsole_command(self):
        self.logfield["state"] = "normal"
        if self.enablePrompts:
            messagebox.showwarning("Warning", "Are you sure you want to clear the console?")
            self.logfield.delete("1.0","end")
        else:
            self.logfield.delete("1.0","end")
        self.logfield["state"] = "disabled"