import json
import os
import shutil

file_path = r'C:\Users\KumarSu\PycharmProjects\turbine_data_sat\turbine_catalogue_productdev.json'
source_folder = r'C:\hpcpool1\Flap\Delta\N175_6220_TCS179N\Flap\N175_6pX_TCS179N_00_6800kW_Mode0\Runs\5\ToolOutput'
destination_folder = r'C:\Users\KumarSu\PycharmProjects\turbine_data_sat\InterpolationData\N163_6pX_TS113_00_NR81_IECS'
with open(file_path, "r") as file:
    json_data = json.load(file)

# turbine Entries
new_turbine_name = "N163_6pX_TS113_00_NR81_60Hz_mode00c1_7000kW"
new_turbine_mode = "mode00c1_7000kw"
# load info Entries
windbin_values = [4.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0]
designwindconditionid_value = "IEC_Ed3_S_N163_6X_TS113_00_mode00"
# Interpolation Folder Entries (.json)
Modelheight = 118
sub_folder_name = "mode 00c1 (7000kW)"

turbine_keys = [key for key in json_data["turbines"] if key.startswith("N163_6pX_TS113_00_NR81_IECS")]
Loadinfo_keys = [key for key in json_data["load_info"]]
print("1. with Extrapolation File path")
print("2. without Extrapolation File path")
choice = int(input("Enter choice please :"))
if choice == 1:
    files_to_copy = ['dlc_1p2.extrap.FLAp.mat', 'dlc_1p2.FLAp.mat']
elif choice == 2:
    files_to_copy = ['dlc_1p2.FLAp.mat']
else:
    print("Not a Valid Choice")

print("selected turbine for turbine catalogue changes", turbine_keys)
mode_folder = os.path.join(destination_folder, sub_folder_name)
if os.path.exists(mode_folder):
    print(f"Folder '{mode_folder}' already exists.")
else:
    os.makedirs(mode_folder, exist_ok=True)
    print(f"Folder '{mode_folder}' created successfully.")

try:
    for file in files_to_copy:
        source_file_path = os.path.join(source_folder, file)
        destination_file_path = os.path.join(mode_folder, file)
        shutil.copy(source_file_path, destination_file_path)
        print(f"File '{file}' copied successfully to 'mode00c1' folder.")
except FileNotFoundError:
    print("Source file not found.")
except PermissionError:
    print("Permission denied. Unable to copy the file.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

pathtoflapdata_value = "InterpolationData/" + new_turbine_name + ".json"
# Interpolation folder changes
interpolation_data_pos = destination_folder.find('InterpolationData')
if interpolation_data_pos != -1:
    location_after_interpolation = destination_folder[interpolation_data_pos + len('InterpolationData'):].strip('\\/')
Interpolation_file_path = r"C:\Users\KumarSu\PycharmProjects\turbine_data_sat\InterpolationData" + "\\" + new_turbine_name + ".json"

if choice == 1:
    FLAp_path = "InterpolationData/" + location_after_interpolation + "/" + sub_folder_name + "/dlc_1p2.FLAp.mat"
    Extrapolation_FLAp_path = "InterpolationData/" + location_after_interpolation + "/" + sub_folder_name + "dlc_1p2.extrap.FLAp.mat"
    Interpolationdata = {
        "dlc1p2": {
            "extrapolation_path": Extrapolation_FLAp_path,
            "model_height": Modelheight,
            "path": FLAp_path,
            "type": "fatigue"
        }
    }
elif choice == 2:
    FLAp_path = "InterpolationData/" + location_after_interpolation + "/" + sub_folder_name + "/dlc_1p2.FLAp.mat"
    Interpolationdata = {
        "dlc1p2": {
            # "extrapolation_path": Extrapolation_FLAp_path,
            "model_height": Modelheight,
            "path": FLAp_path,
            "type": "fatigue"
        }
    }

if os.path.exists(Interpolation_file_path):
    print("File already available at:", Interpolation_file_path)
else:
    print("New File at:", Interpolation_file_path)
    with open(Interpolation_file_path, "w") as file:
        json.dump(Interpolationdata, file, indent=4)
print("/n")
for key in turbine_keys:
    if json_data["turbines"][key]["confirmed_modes"] != []:
        if new_turbine_mode not in json_data["turbines"][key]["confirmed_modes"]:
            json_data["turbines"][key]["confirmed_modes"].append(new_turbine_mode)
            print(new_turbine_mode, " - added in confirmed mode")
    if new_turbine_mode not in json_data["turbines"][key]["mode_order"]:
        json_data["turbines"][key]["mode_order"].append(new_turbine_mode)
        print(new_turbine_mode, " - added in mode order of ", key)
    if new_turbine_mode in json_data["turbines"][key]["unavailable_modes"]:
        json_data["turbines"][key]["unavailable_modes"].remove(new_turbine_mode)
        print(new_turbine_mode, " - removed in unavailable mode of ", key)
    if new_turbine_name not in json_data["turbines"][key]["load_info"]:
        json_data["turbines"][key]["load_info"][new_turbine_name] = [new_turbine_mode]
        print(new_turbine_mode, " - added in load info of", key)
    # else:
    #     json_data["turbines"][key]["load_info"][new_turbine_name].append(new_turbine_mode)
    # json_data["turbines"][key]["load_info"]["N163_5pX_TS125_06_NR81_60Hz_new_4930kW"] = ["mode05_4930kw"]

print("\n")
if new_turbine_name not in Loadinfo_keys:
    json_data["load_info"][new_turbine_name] = {
            "analysis_method": "ccd",
            "design_life_time_in_years": 20.0,
            "design_wind_condition_id": designwindconditionid_value,
            "extreme_load_cases": [],
            "fatigue_load_cases": ["dlc1p2"],
            "path_to_flap_data": pathtoflapdata_value,
            "reference_wind_condition_id": "FLAp_BigTI",
            "seconds_per_time_unit": 3600,
            "windbin_centers": windbin_values,
            "woehler_for_ieff": [1, 3.0, 3.3, 4.0, 5.0, 6.6, 7.0, 8.7, 9.0, 10, 11, 14]
        }
    print(new_turbine_name, " - added in load info master key")
# Convert the modified JSON data back to a string
with open(file_path, "w") as file:
    json.dump(json_data, file, indent=4)


print("\n")
print("JSON file created and saved at:", Interpolation_file_path)
# updated_data = json.dumps(json_data, indent=4)
# Print the updated JSON
# print("Changes saved to turbineinfo.json.", updated_data)







