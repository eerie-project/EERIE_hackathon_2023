from copy import deepcopy
def find_data_sources(catalog,name=None):
    newname='.'.join(
        [ a 
         for a in [name, catalog.name]
         if a
        ]
    )
    data_sources = []

    for key, entry in catalog.items():
        if isinstance(entry, intake.catalog.Catalog):
            if newname == "main":
                newname = None
            # If the entry is a subcatalog, recursively search it
            data_sources.extend(find_data_sources(entry, newname))
        elif isinstance(entry, intake.source.base.DataSource):
            data_sources.append(newname+"."+key)

    return data_sources
