from prsync.gui.screen import Gui


def validate_new_session(gui: Gui) -> int:
    return 0 if all(
        gui.credentials_inputs[cred_group][param].get() for cred_group in gui.credentials_inputs for param in
        gui.credentials_inputs[cred_group]
    ) else 1