import time
import flet as ft


is_dark_mode = True

def send_message(page: ft.Page, message_liste: ft.Column, message_entre: ft.TextField):
    # Affichage du message
    q = str(message_entre.value)
    message_liste.controls.append(ft.Row([
        ft.Container(content=ft.Text(message_entre.value), bgcolor=ft.colors.LIGHT_BLUE, padding=10, border_radius=10),
        ft.Container(content=ft.Text("You"), bgcolor=ft.colors.LIGHT_BLUE_ACCENT, padding=5, border_radius=5, margin=ft.margin.only(left=10))
    ], alignment=ft.MainAxisAlignment.END))
    page.splash.visible = True
    page.update()
    time.sleep(5)
    #######################
    ## Reponse du bot #####
    repMax = "read"
    # Ajout de la réponse #
    #######################
    message_liste.controls.append(ft.Row([
        ft.Container(content=ft.Image("static/images/max.png", width=25,height=25,fit=ft.ImageFit.CONTAIN,), bgcolor=ft.colors.WHITE, padding=5, border_radius=5, margin=ft.margin.only(left=10)),
        ft.Container(content=ft.Text(repMax), bgcolor=ft.colors.GREY, padding=10, border_radius=10),
    ], alignment=ft.MainAxisAlignment.START))
    # Mise à jour de la page
    message_entre.value = ""
    page.splash.visible = False
    message_entre.update()
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
    page.title = "J'ai quoi ?"
    page.theme_mode = "dark"
    page.splash = ft.ProgressBar(visible=False)
    
    # Chat interface

    #######################
    ####### Objets ########
    #######################

    message_liste = ft.Column(expand=1, wrap=False, scroll="always")
    message_entre = ft.TextField(hint_text="Type a message...", on_submit=lambda e: send_message(page, message_liste, message_entre))
    envoyerBoutton = ft.ElevatedButton("Send", on_click=lambda e: send_message(page, message_liste, message_entre,))    
    
    toggledarklight = ft.IconButton(on_click=lambda e: switch_theme(page, is_dark_mode),icon="dark_mode",selected_icon="light_mode",style=ft.ButtonStyle(color={"":ft.colors.BLACK,"selected":ft.colors.WHITE}))
    entete = ft.AppBar(title=ft.Text("J'ai quoi ?",size=30,color="black"),bgcolor="Yellow",leading=ft.IconButton(icon="Chat"),actions=[toggledarklight ])

    #######################

    page.add(entete, message_liste, message_entre, envoyerBoutton, )
    page.update()

ft.app(target=main, view=ft.AppView.FLET_APP)