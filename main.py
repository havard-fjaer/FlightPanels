from panels.panel_controller import PanelController
from panels.radio_panel import RadioPanel
import panel_mapping

def main():
    panel_controller = PanelController()
    panel_controller.append(panel_mapping.create_radio_panel_1)
    panel_controller.append(panel_mapping.create_radio_panel_2)
    panel_controller.start_all()
    panel_controller.wait()

if __name__ == "__main__":
    main()
