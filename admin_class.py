class Admin:
    def __init__(self, user_id, *websites):
        self.id = user_id
        self.websites = {}
        for website in list(websites):
            self.websites[website] = [website,1]
    
    def add_web(self, website):
        if website not in self.websites:
            self.websites[website] = [website,1]
            return self.websites
        elif self.websites[website][1] == 0:
            self.websites[website][1] = 1
            return self.websites
        else:
            return None
    
    def del_web(self, website):
        if website in self.websites:
            self.websites[website] = [website,0]
            return self.websites
        else:
            return None
    
    def __str__(self):
        string = f""
        for website in self.websites:
            if self.websites[website][1] == 1:
                string += f"{self.websites[website][0]}\n\n"
        if len(string) == 0:
            return "No websites are being monitored right now."
        else:
            return f"Here is the list of your websites:\n\n"+string