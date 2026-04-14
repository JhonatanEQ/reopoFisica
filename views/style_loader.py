import os

class StyleLoader:
    @staticmethod
    def load_styles(styles_dir="views/styles"):
        """
        Lee todos los archivos .qss en el directorio especificado y los combina.
        """
        combined_qss = ""
        # Orden sugerido: variables, base, controls, cards, main
        order = ["variables.qss", "base.qss", "controls.qss", "cards.qss", "main.qss"]
        

        for filename in order:
            filepath = os.path.join(styles_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    combined_qss += f.read() + "\n"
        

        for filename in os.listdir(styles_dir):
            if filename.endswith(".qss") and filename not in order:
                filepath = os.path.join(styles_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    combined_qss += f.read() + "\n"
                    
        return combined_qss
