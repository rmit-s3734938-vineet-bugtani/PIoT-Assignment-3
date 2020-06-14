import unittest
import socketio
import sys, json
import cv2
from pyzbar.pyzbar import decode

class Agent_Tests(unittest.TestCase):
    client = socketio.Client() #Test socket client
    ip = None
    carID = None

    # Config and testing methods
    def load_config(self) :
        """ 
        Loads json config from config.json
        """
        try:
            with open("config.json") as f:
                data = json.load(f)
                self.ip = "http://" + data["host"] + ":" + data["port"]
                self.carID = data["carID"]
        except Exception as e:
            print(str(e))
            sys.exit("Error when reading from Json.")
    
    # Connect to testing namespace
    def connect(self) : 
        self.client.connect(self.ip, namespaces=['/test'])
    
    # QR method
    def getUsernameFromQR(self, imageName):
        # This will change - not sure whether mac needs full path or some other issues.
        image = cv2.imread('./QRCodes/' + imageName)
        for barcode in decode(image):
            username = barcode.data.decode('utf-8')
            return username

    # Before All
    @classmethod
    def setUpClass(self):
        self.load_config(self)
        self.connect(self)
    
    # After All
    @classmethod
    def tearDownClass(self):
        self.client.disconnect()
        exit

    # Tests require master server to be running
    
    """
    Test socket connection with master.

    Checks for sid after connecting
    """
    def test_Socket_Connection(self):
        sid = self.client.sid
        self.assertTrue(sid)

    
    """
    Test retrieving authorized devices list.

    Checks for list after retrieving
    """
    def test_Maclist_Return(self):
        mac_list = self.client.call('maclist')
        self.assertTrue(mac_list)
    
    """
    Test for appropriate response to unauthorized address

    Checks if address is in mac_list
    """
    def test_Unauth_Address(self):
        mac_list = self.client.call('maclist')
        mac = "TH:IS:IS:FA:KE"
        auth = False
        if mac in mac_list:
            auth = True
        self.assertFalse(auth)

    """
    Test unknown QR code image

    Scans a QR code containing a username not in database and asserts correct response
    """
    def test_QR_Profile_Incorrect(self):
        imageName = "fakename.png"
        username = self.getUsernameFromQR(imageName)
        found, profile = self.client.call('qr_profile', data=username)
        self.assertFalse(found)
    
    """
    Test known QR code image

    Scans a QR code containing a username in database and asserts correct response
    """
    def test_QR_Profile_Correct(self):
        imageName = "mWoods.png"
        username = self.getUsernameFromQR(imageName)
        found, profile = self.client.call('qr_profile', data=username)
        self.assertTrue(found)

if __name__ == "__main__":
    unittest.main()