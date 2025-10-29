from views.exportarView import ExportarView

class ExportarVM:
    def __init__(self, master):

        self.export = ExportarView(master)
        self.export.pack(fill="x", padx=10, pady=10)
