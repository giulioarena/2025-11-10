import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.k = 0


    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        if self._view._txtIntK.value is None or "." in self._view._txtIntK.value or "," in self._view._txtIntK.value:
            self._view.txt_result.controls.append(ft.Text(f"Inserire un numero intero", color="red"))
            self._view.update_page()
            return
        try:
            self.k = int(self._view._txtIntK.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text(f"Inserire un numero intero", color = "red"))
            self._view.update_page()
            return

        self._model.buildGraph(int(self._view._ddStore.value), self.k)
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente | #nodi: {len(self._model.graph.nodes)}, #archi: {len(self._model.graph.edges)}", color="blue"))
        heaviest = self._model.get5Heaviest()
        self._view.txt_result.controls.append(ft.Text(f"I 5 archi più pesanti sono:"))
        for e in heaviest:
            self._view.txt_result.controls.append(ft.Text(f"{e[0]} --> {e[1]} | weight = {e[2]["weight"]}"))

        self.fillDDNode()
        self._view._ddNode.disabled = False

        self._view.update_page()


    def handleCerca(self, e):
        src_id = self._view._ddNode.value
        path = self._model.getLongestPath(src_id)
        self._view.txt_result.controls.append(ft.Text(f"\nTrovato il cammino più lungo | lenght = {len(path)}", color="blue"))
        output = ""
        for n in path:
            output += f"{n} -> "
        output = output.rstrip(" -> ")
        self._view.txt_result.controls.append(ft.Text(f"{output}"))
        self._view.update_page()

    def handleRicorsione(self, e):
        src_id = self._view._ddNode.value
        path = self._model.getHeaviestPath(src_id)
        self._view.txt_result.controls.append(
            ft.Text(f"\nTrovato il cammino più pesante | weight = {self._model.peso(path)}", color="blue"))
        output = ""
        for n in path:
            output += f"{n} -> "
        output = output.rstrip(" -> ")
        self._view.txt_result.controls.append(ft.Text(f"{output}"))
        self._view.update_page()

    def fillDDStore(self):
        stores = self._model.getAllStores()
        storesDD = [ft.dropdown.Option(key=s.store_id, text=s.store_name) for s in stores]
        self._view._ddStore.options = storesDD

    def fillDDNode(self):
        nodes = list(self._model.graph.nodes)
        nodesDD = [ft.dropdown.Option(key=n.order_id, text=n) for n in nodes]
        self._view._ddNode.options = nodesDD

    def abilitateCerca(self, e):
        self._view._btnCerca.disabled = False
        self._view._btnRicorsione.disabled = False
        self._view.update_page()
