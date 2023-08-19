import logging
import os
import subprocess
import sys

import PySimpleGUI as sg

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def check_dependencies():
    text = "Checkeando dependencias:\n"

    # Check ffmpeg
    result = subprocess.run("ffmpeg -version", shell=True, capture_output=True, text=True)
    ffmpeg_installed = not bool(result.stderr)
    text += (
        "- `ffmpeg` está instalado"
        if ffmpeg_installed
        else "- `ffmpeg` no está instalado. Puede instalarlo con \n\tsudo apt install ffmpeg"
    )

    # text += "\n"

    # # Check tk
    # try:
    #     import tkinter as _

    #     tk_installed = True
    # except ImportError:
    #     tk_installed = False
    # text += (
    #     "- `tkinter` está instalado"
    #     if ffmpeg_installed
    #     else "- `tkinter` no está instalado. Puede instalarlo con \n\tsudo apt install python3-tk"
    # )

    success = ffmpeg_installed  # and tk_installed

    return (success, text)


def split_audio(file, output_folder, segment_time):
    extension = os.path.splitext(file)[1]
    filebasename_noextension = os.path.basename(os.path.splitext(file)[0])

    cmd = [
        f"ffmpeg -i '{file}' -f segment -segment_time {segment_time} -c copy '{output_folder}/{filebasename_noextension}%04d{extension}' -loglevel error -hide_banner"
    ]
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
    )
    return result


def initialize_gui():
    sg.theme("DarkBlue")
    layout = [
        [sg.Text("Corta audios 🎙️🪚", justification="center", font="Bold 20")],  # TODO: center
        [
            sg.Text("Archivo de entrada:"),
            sg.Combo(
                sg.user_settings_get_entry("-filenames-", []),
                default_value=sg.user_settings_get_entry("-last file-", ""),
                size=(50, 1),
                key="-FILENAME-",
                enable_events=True,
            ),  # Text box
            sg.FileBrowse(button_text="Elegir"),  # Browser button
        ],
        [
            sg.Text("Longitud del segmento:"),
            sg.Input(key="-segment-", default_text="60", size=4),
            sg.Text("segundos"),
        ],
        [
            sg.Text("Carpeta de salida:"),
            sg.Combo(
                sg.user_settings_get_entry("-foldernames-", []),
                default_value=sg.user_settings_get_entry("-last foldername-", ""),
                size=(50, 1),
                key="-FOLDERNAME-",
            ),  # Text box
            sg.FolderBrowse(button_text="Elegir"),  # Browser button
        ],
        [sg.Button("Separar")],
        [sg.Col(key="-COL-", layout=[])],
    ]

    window = sg.Window("🎙️🪚", layout)

    return (window, layout)


def add_text_to_column(window, sg_text, key="-COL-"):
    window.extend_layout(window["-COL-"], [[sg_text]])


def loop(window):
    while True:
        event, values = window.read()

        logger.debug(f"event: {event}\nvalues: {values}")

        if event == sg.WIN_CLOSED:
            break

        elif event == "Separar":
            file = values["-FILENAME-"]
            foldername = values["-FOLDERNAME-"]
            segment_time = values["-segment-"]
            # Save file to history
            sg.user_settings_set_entry(
                "-filenames-",
                list(
                    set(
                        sg.user_settings_get_entry("-filenames-", [])
                        + [
                            file,
                        ]
                    )
                ),
            )
            sg.user_settings_set_entry("-last file-", file)
            # window["-FILENAME-"].update(values=list(set(sg.user_settings_get_entry("-filenames-", [])))) # Clear input
            # Save folderename to history
            sg.user_settings_set_entry(
                "-foldernames-",
                list(
                    set(
                        sg.user_settings_get_entry("-foldernames-", [])
                        + [
                            foldername,
                        ]
                    )
                ),
            )
            sg.user_settings_set_entry("-last foldername-", foldername)
            # window["-FOLDERNAME-"].update(values=list(set(sg.user_settings_get_entry("-foldernames-", [])))) # Clear input

            # split audio
            output = split_audio(file, foldername, segment_time)
            logger.debug(output)
            if output.stderr:
                text = f"Error separando audio: {output.stderr}"
                logger.error(text)
                add_text_to_column(
                    window=window, sg_text=sg.Text(text=text, text_color="red", font="Mono 10")
                )
            else:
                text = f"Separación existosa"
                logger.info(text)
                add_text_to_column(window=window, sg_text=sg.Text(text=text))

        elif event == "-FILENAME-":  # User selected a folder
            directory_path = os.path.dirname(values["-FILENAME-"])
            window["-FOLDERNAME-"].update(value=directory_path)


def main():
    deps_installed, deps_text = check_dependencies()
    if deps_installed:
        logger.info(deps_text)
    else:
        logger.error(deps_text)
        sys.exit(1)

    window, _ = initialize_gui()

    loop(window)


if __name__ == "__main__":
    main()
