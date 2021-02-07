from panels.panel_controller import PanelController
from panels.radio_panel import RadioPanel
from demo.radio_panel_demo import RadioPanelDemoService

def main():
    panel_controller = PanelController()
    panel_controller.append(RadioPanel(RadioPanelDemoService(), usb_bus=0, usb_address=3))
    panel_controller.append(RadioPanel(RadioPanelDemoService(), usb_bus=0, usb_address=4))
    panel_controller.start_all()
    panel_controller.wait()

if __name__ == "__main__":
    main()
