import time
import flet as ft
import main_backend as mb

# Variables

is_dark_mode = True

index = 0
maladies_responsables_listes = []
medicaments_responsables_listes = []

historique = ["Acute abdomen", "Aortitis syndrome"]

# Fonctions

def change_theme(page: ft.Page, is_dark_mode: bool):
    page.theme_mode = "light" if page.theme_mode =="dark" else "dark"
    # SWITCH THE THEME
    if is_dark_mode:
        is_dark_mode = False
    else:
        is_dark_mode = True
    page.update()



def fermer_recherche(Recherche: ft.SearchBar, e):
        text = f"{e.control.data}"
        Recherche.close_view(text)


# Main
    
def main(page: ft.Page):
    page.title = "J'ai Quoi ?"
    page.theme_mode = "dark"
    
    # objets

    changeurTheme = ft.Switch(
        adaptive=True,
        value=True,
        on_change=lambda e: change_theme(page, is_dark_mode),
    )

    Recherche = ft.SearchBar(
        view_elevation=1,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Rechercher symptomes...",
        # Recuperer le texte de la recherche
        on_submit=lambda e: rechercher(page, Recherche, e,maladies_responsables_tab, medicaments_responsables_tab),
        controls=[
            ft.ListTile(title=ft.Text(f"{i}"), on_click=lambda e: fermer_recherche(Recherche,e), data=i)
            for i in historique # On peut mettre nos exemples ici
        ],
    )


    Titre = ft.AppBar(
        leading=ft.Icon(ft.icons.LOCAL_HOSPITAL),
        leading_width=40,
        title=ft.Text("J'ai QUOI ?"),
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[changeurTheme,]
    )

    Menu = ft.CupertinoSlidingSegmentedButton(
        selected_index=0,
        thumb_color=ft.colors.BLUE_400,
        on_change=lambda e: changerAffichage(page, maladies_responsables_tab, medicaments_responsables_tab),
        controls=[
            ft.Text("Maladies responsables"),
            ft.Text("Médicaments responsables"),
        ],
    )
    #######

    def changerAffichage(page: ft.Page, maladies_responsables_tab, medicaments_responsables_tab):
        global index
        if index == 0:
            index = 1
            page.controls.pop()
            medicaments_responsables_tab = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Nom du médicament")),
                    ft.DataColumn(ft.Text("Source")),
                    # ft.DataColumn(ft.Text("Score"), numeric=True),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.ElevatedButton(medicament[1], on_click=show_bs)),
                            ft.DataCell(ft.Text(medicament[0])),
                            # ft.DataCell(ft.Text(medicament[2])),
                        ]
                    )
                    for medicament in medicaments_responsables_listes
                ],
            )
            page.add(medicaments_responsables_tab)
            page.update()
        else:
            index = 0
            page.controls.pop()
            maladies_responsables_tab = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Nom de la maladie")),
                    ft.DataColumn(ft.Text("Source")),
                    # ft.DataColumn(ft.Text("Score"), numeric=True),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.ElevatedButton(maladie[1], on_click=show_bs)),
                            ft.DataCell(ft.Text(maladie[0])),
                            # ft.DataCell(ft.Text(maladie[2])),
                        ]
                    )
                    for maladie in maladies_responsables_listes
                ],
            )
            page.add(maladies_responsables_tab)
            page.update()

    def rechercher(page, Recherche: ft.SearchBar , e, maladies_responsables_tab, medicaments_responsables_tab):
        global historique
        global index
        Recherche.close_view(e.data)
        print("Recherche en cours...")
        #chargement
        global maladies_responsables_listes
        global medicaments_responsables_listes
        maladies_responsables_listes, medicaments_responsables_listes = mb.rechercherDonnee(e.data)
        if index == 0:
            index = 1
            changerAffichage(page, maladies_responsables_tab, medicaments_responsables_tab)
        else:
            index = 0
            changerAffichage(page, maladies_responsables_tab, medicaments_responsables_tab)
        indice = -1
        
        taille = len(historique)
        for i in range(taille):
            if historique[i] == e.data:
                indice = i
                break
        if indice != -1:
            historique.pop(indice)
            historique = [e.data] + historique
        else: 
            if taille == 5:
                historique = [e.data] + historique[:4]
            else:
                historique = [e.data] + historique
        Recherche.controls = [ft.ListTile(title=ft.Text(f"{i}"), on_click=lambda e: fermer_recherche(Recherche,e), data=i)
            for i in historique # On peut mettre nos exemples ici
        ]
        print("Recherche terminée")
        page.update()


    def bs_dismissed(e):
        print("Dismissed!")

    def show_bs(e):
        bs.open = True
        bs.update()

    def close_bs(e):
        bs.open = False
        bs.update()

    bs = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("This is sheet's content!"),
                    ft.ElevatedButton("Close bottom sheet", on_click=close_bs),
                ],
                tight=True,
            ),
            padding=10,
        ),
        open=False,
        on_dismiss=bs_dismissed,
    )
    page.overlay.append(bs)


    #######

    # Conteneur qui contient une liste de maladies sous forme de boutons




    maladies_responsables_tab = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nom de la maladie")),
                ft.DataColumn(ft.Text("Source")),
                # ft.DataColumn(ft.Text("Score"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.ElevatedButton(maladie[1], on_click=show_bs)),
                        ft.DataCell(ft.Text(maladie[0])),
                        # ft.DataCell(ft.Text(maladie[2])),
                    ]
                )
                for maladie in maladies_responsables_listes
            ],
        )
    
    medicaments_responsables_tab = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nom du médicament")),
                ft.DataColumn(ft.Text("Source")),
                # ft.DataColumn(ft.Text("Score"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.ElevatedButton(medicament[1], on_click=show_bs)),
                        ft.DataCell(ft.Text(medicament[0])),
                        # ft.DataCell(ft.Text(medicament[2])),
                    ]
                )
                for medicament in medicaments_responsables_listes
            ],
        )

    page.add(Titre, Recherche, Menu, maladies_responsables_tab)
    page.update()         


ft.app(target=main, view=ft.AppView.FLET_APP)