class AreaStore():

    def __init__(self,name):
        self.name = name
        self.devices_names = []
        self.elec_devices_names = []
        self.devices = []
        self.elec_devices = []

    def add_elec_device_name(self, elec_device):
        self.elec_devices_names.append(elec_device)

    def add_device_name(self, device):
        self.devices_names.append(device)

    # def add_device(self, area_name, device):
    #     area = self.get_area(area_name)
    #     if area is None:
    #         area = Area(area_name)
    #         area.add_device(device)
    #         self.areas.append(area)
    #     else:
    #         area.add_device(device)

    def get_area(self, area):
        for a in self.areas:
            if a.area == area:
                return a
        return None

    def to_dict(self):
        return{
            'name': self.name,
            'elec_devices_names': self.elec_devices_names,
            'devices_names': self.devices_names,
  
        } 
        
        
        #   'devices': [item.to_dict() for item in self.areas]
class Area():
    def __init__(self,area):
        self.area = area
        self.devices = []

    def add_device(self,device):
        self.devices.append(device)

    def to_dict(self):
        return {
            'area': self.area,
            'devices': self.devices
        }
    