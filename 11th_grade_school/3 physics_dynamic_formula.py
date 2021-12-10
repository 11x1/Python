allowed_parameters = ["a", "v", "v0", "t"]
param_values = {}
i = 0
while i < 3:
    val = input(f"Sisestage parameeter {allowed_parameters}: ")
    while int(val.split("=")[1]) < 0:
        val = input(f"Sisestage parameeter {allowed_parameters}: ")

    if val.split("=")[0] in allowed_parameters:
        allowed_parameters.pop(allowed_parameters.index(val.split("=")[0]))
        param_values[val.split("=")[0]] = int(val.split("=")[1])
    i += 1

not_used_param = allowed_parameters[0]
if not_used_param == "a":
    param_values[not_used_param] = (param_values["v"] - param_values["v0"]) / param_values["t"]
elif not_used_param == "v":
    param_values[not_used_param] = (param_values["a"] * param_values["t"]) + param_values["v0"]
elif not_used_param == "v0":
    param_values[not_used_param] = -1 * ((param_values["a"] * param_values["t"]) - param_values["v"])
elif not_used_param == "t":
    param_values[not_used_param] = (param_values["v"] - param_values["v0"]) / param_values["a"]

print(f"{not_used_param} = {param_values[not_used_param]}")
