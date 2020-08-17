import pandas as pd


class finder():
    # displayer class manage calculation of display of information

    def __init__(self, compounds_file="compounds.csv"):
        try:
            self.compounds = pd.read_csv(
                compounds_file, encoding='utf-8', dtype=str)
        except:
            self.compounds = pd.DataFrame({"compound": [], "component": []})

    def explode_topic(self, topic):
        ttopic = topic.split(sep="/", maxsplit=1)
        if len(ttopic) == 1:
            return {"base": ttopic[0], "info": ""}
        else:
            return {"base": ttopic[0], "info": ttopic[1]}

    def search_components(self, compound):
        return list(self.compounds["component"][self.compounds["compound"] == compound])

    def display_components(self, components, color):
        return
