import PySimpleGUI as sg

class sw_Button(sg.Button):
    def __init__(self,button_text,button_key,**kwargs):
        super().__init__(button_text = button_text,key=button_key,button_color=("white","green"),**kwargs)
        pass
    
    def ButtonCallBack(self):
        self.toggle()
        return super().ButtonCallBack()
    
    def toggle(self):
        #print(self.ButtonColor)
        match self.ButtonColor[1]:
            case "red":
                self.update(button_color = "green",text = "Start")
            case "green":
                self.update(button_color = "red",text = "Stop")
        pass