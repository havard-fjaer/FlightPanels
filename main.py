from panels.panel_controller import PanelController
import panel_mapping

def main():
    controller = PanelController()
    controller.add_panel(panel_mapping.create_radio_panel_1())
    controller.add_panel(panel_mapping.create_radio_panel_2())
    controller.wait()

if __name__ == "__main__":
    main()
