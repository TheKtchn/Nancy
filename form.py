

def form(template):
    response = {"error": False, "data": None}

    for t in template:
        variable = input(f"{t['prompt']}: ").strip()
        datatype = t["datatype"]

        if datatype == "string":
            if not variable:
                response["error"] = True
                return response

        elif datatype == "currency":
            try:
                variable = abs(float(variable))
            except Exception as e:
                response["error"] = True
                return response

        elif datatype == "date":
            try:
                variable = abs(float(variable))
            except Exception as e:
                response["error"] = True
                return response
        response["data"][t["variable"]] = variable
