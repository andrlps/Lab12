import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._anno = None
        self._nazione = None
        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        for i in range(2015,2019):
            self._view.ddyear.options.append(ft.dropdown.Option(i))
        for nazione in DAO.getNazioni():
            self._view.ddcountry.options.append(ft.dropdown.Option(nazione))
        self._view.update_page()


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        self._anno = self._view.ddyear.value
        self._nazione = self._view.ddcountry.value
        if self._nazione is None or self._anno is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un anno e un retailer prima di procedere alla creazione del grafo.", color="red"))
            self._view.update_page()
            return
        self._model.builGraph(self._anno, self._nazione)
        numNodi, numArchi = self._model.getInfoGraph()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato con {numNodi} nodi e {numArchi} archi."))
        self._view.update_page()

    def handle_volume(self, e):
        if self._nazione is None or self._anno is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un anno e un retailer prima di procedere alla creazione del grafo.", color="red"))
            self._view.update_page()
            return
        if self._model.getVolumeVendita() is None:
            self._view.txt_result.controls.append(
                ft.Text("Procedere alla creazione del grafo.", color="red"))
            self._view.update_page()
            return
        for r in self._model.getVolumeVendita():
            self._view.txtOut2.controls.append(
                ft.Text(f"{r[0]} - {r[1]}"))
        self._view.update_page()


    def handle_path(self, e):
        pass