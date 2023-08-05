def clean_nb(dirty, preserve=True):
    cells = dirty.get('cells', [])
    for cell in cells:
        if cell["cell_type"] != "code": continue
        cell["execution_count"] = None
        if preserve:
            if not cell["source"] or not cell["source"][0].strip().endswith("preserve"):
                cell["outputs"] = []
        else:
            cell["outputs"] = []
