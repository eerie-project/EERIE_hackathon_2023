import  intake
def search(cat, searchdict = {}):
        """Search a yaml catalog cat by providing a key-value search dictionary.
        Keys must match metadata keys exactly, for values regexp findall is used
        variable_names = temp will match variable_names = temp or global_temperature
        variable_names = glo.*temp will match variable_names = "global_temperature", but not "temperature"
        var = temperature will not match variable_names = temperature
        """
        import logging
        yaml_searcher.all_keys = set()
        yaml_searcher.keys_found = { k: False for k in searchdict.keys() }
        yaml_searcher._search(cat, searchdict)
        for k, v in yaml_searcher.keys_found.items():
            if v == False:
                logging.error ( f"Found no metadata key matching {k}")
                logging.error ( "Possible keys:")
                logging.error ("\n    ".join(sorted(yaml_searcher.all_keys)) + "\n")

class yaml_searcher:
    def _search ( cat, searchdict = {}, prefix = ""):
        import logging
        import re
        for x in cat:
            logging.debug (prefix + x)
            try:
                cat[x] is None
            except:
                logging.error( f"Can't access subcatalog {x}")
                continue
            if x in ("observations", "archive", "cloud", "jasmin", "main", "ERA5"):
                logging.warning (f"skipping {x} for now")
                continue
            elif type (cat[x]) is intake.catalog.local.YAMLFileCatalog:
                print ((prefix + x))
                yaml_searcher._search(cat[x], searchdict, prefix+"   ")
            else:
                try:
                    md = cat[x].metadata
                    found = True
                    hits  = ""
                    for k, v in searchdict.items():
                        hits = {}
                        if k in md.keys():
                            yaml_searcher.keys_found[k] = True
                            vfound = []
                            for vv in md[k]:
                                if re.findall(v,vv):
                                    vfound.append(vv)
                            if len (vfound):
                                hits [k] = vfound
                            else:
                                found = False
                        else:
                            found = False
                            yaml_searcher.all_keys = yaml_searcher.all_keys | set(md.keys())
                    if found == True:
                        print (prefix + x, hits)
                        found_any = True
                except Exception as e:
                    logging.warning(f"can't process {x} of type {type(cat[x])}")
                    logging.warning(e)