import time
import flet as ft


is_dark_mode = True


def send_message(page, message_list, message_input):
    # Affichage du message
    q = str(message_input.value)
    message_list.controls.append(ft.Row([
        ft.Container(content=ft.Text(message_input.value), bgcolor=ft.colors.LIGHT_BLUE, padding=10, border_radius=10),
        ft.Container(content=ft.Text("You"), bgcolor=ft.colors.LIGHT_BLUE_ACCENT, padding=5, border_radius=5, margin=ft.margin.only(left=10))
    ], alignment=ft.MainAxisAlignment.END))
    repMax = "read"
    message_list.controls.append(ft.Row([
        ft.Container(content=ft.Image("static/images/max.png", width=25,height=25,fit=ft.ImageFit.CONTAIN,), bgcolor=ft.colors.WHITE, padding=5, border_radius=5, margin=ft.margin.only(left=10)),
        ft.Container(content=ft.Text(repMax), bgcolor=ft.colors.GREY, padding=10, border_radius=10),
    ], alignment=ft.MainAxisAlignment.START))
    # Mise à jour de la page
    message_input.value = ""
    message_input.update()
    page.update()


def switch_theme(page: ft.Page, is_dark_mode: bool):
    page.theme_mode = "light" if page.theme_mode =="dark" else "dark"
    page.update()
    time.sleep(0.5)
    # SWITCH THE THEME
    if is_dark_mode:
        is_dark_mode = False
    else:
        is_dark_mode = True
    page.splash.visible = False
    # AND PAGE UPDATE FOR CHANGE STATE
    page.update()




def main(page: ft.Page):
    page.title = "BioGuess"
    page.theme_mode = "dark"
    page.splash = ft.ProgressBar(visible=False)
    
    # Chat interface

    #######################
    ####### Objects #######
    #######################

    message_list = ft.Column(expand=1, wrap=False, scroll="always")
    message_input = ft.TextField(hint_text="Type a message...", on_submit=lambda e: send_message(page, message_list, message_input))
    send_button = ft.ElevatedButton("Send", on_click=lambda e: send_message(page, message_list, message_input,))    
    
    toggledarklight = ft.IconButton(on_click=lambda e: switch_theme(page, is_dark_mode),icon="dark_mode",selected_icon="light_mode",style=ft.ButtonStyle(color={"":ft.colors.BLACK,"selected":ft.colors.WHITE}))
    head = ft.AppBar(title=ft.Text("Chat",size=30),bgcolor="Yellow",leading=ft.IconButton(icon="menu"),actions=[toggledarklight ])

    navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.CHAT, label="Chat"),
            ft.NavigationDestination(icon=ft.icons.MUSIC_NOTE, label="Singer"),
            ft.NavigationDestination(icon=ft.icons.BOOK_SHARP,label="Lessons",),
        ]
    )

    #######################

    page.add(head, message_list, message_input, send_button, navigation_bar)
    page.update()


ft.app(target=main, view=ft.AppView.FLET_APP)