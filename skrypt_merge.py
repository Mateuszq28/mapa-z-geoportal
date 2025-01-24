from osgeo import gdal
import numpy as np
from PIL import Image

# Ścieżki do plików .asc
sektor1_path = "dabrowa_lewo.asc"
sektor2_path = "wk_prawo.asc"

# Wczytanie plików .asc
sektor1 = gdal.Open(sektor1_path)
sektor2 = gdal.Open(sektor2_path)

# Odczyt danych jako tablic NumPy
array1 = sektor1.ReadAsArray()
array2 = sektor2.ReadAsArray()

def print_diagnostics(array1, array2):
    # Diagnostyka - zakresy danych
    print("Sektor 1 - min:", np.min(array1), "max:", np.max(array1))
    print("Sektor 2 - min:", np.min(array2), "max:", np.max(array2))
    min_global = min(np.min(array1), np.min(array2))
    max_global = max(np.max(array1), np.max(array2))
    print("Global - min:", min_global, "max:", max_global)
print_diagnostics(array1, array2)

# Diagnostyka - zakresy danych
print("Po odrzuceniu -9999:")
print("Sektor 1 - min:", np.min(array1[array1 > -9999]), "max:", np.max(array1[array1 > -9999]))
print("Sektor 2 - min:", np.min(array2[array2 > -9999]), "max:", np.max(array2[array2 > -9999]))

# Zamiana wartości brakujących (-9999) na zero
# array1[array1 == -9999] = 0
# array2[array2 == -9999] = 0

# Przycinanie sektorów do najmniejszego wspólnego rozmiaru
def cut_to_min_size(array1, array2):
    min_rows = min(array1.shape[0], array2.shape[0])
    min_cols = min(array1.shape[1], array2.shape[1])
    return array1[:min_rows, :min_cols], array2[:min_rows, :min_cols]

array1, array2 = cut_to_min_size(array1, array2)

def crop_margin(array, margin=30):
    return array[margin:-margin, margin:-margin]

array1 = crop_margin(array1)
array2 = crop_margin(array2)

# Twarde skalowanie wartości (zakres od 0 do 1000)
def hard_scale(array, min_value=0, max_value=1000):
    array = np.clip(array, min_value, max_value)
    scaled_array = ((array - min_value) / (max_value - min_value) * 255).astype(np.uint16)
    return scaled_array

# array1 = hard_scale(array1)
# array2 = hard_scale(array2)

def replace_negative_with_min(array):
    min_value = min(array[array > -9999])
    array[array <= -9999] = min_value
    return array

array1 = replace_negative_with_min(array1)
array2 = replace_negative_with_min(array2)

# Diagnostyka - zakresy danych
print("po podmianie min")
print_diagnostics(array1, array2)


def min_max_scale(array, min_value=0, max_value=255):
    array = np.clip(array, min_value, max_value)
    scaled_array = ((array - min(array.flatten())) / (max(array.flatten()) - min(array.flatten())) * 255).astype(np.uint16)
    return scaled_array

array1 = min_max_scale(array1)
array2 = min_max_scale(array2)

def margins(array1, array2):
    array1_right_margin_avg = np.mean(array1[:, -30:]).astype(np.int16)
    array2_left_margin_avg = np.mean(array2[:, :30]).astype(np.int16)
    print("array1_right_margin_avg:", array1_right_margin_avg)
    print("array2_left_margin_avg:", array2_left_margin_avg)
    print(type(array1_right_margin_avg))
    print(type(array2_left_margin_avg))
    diff = np.abs(array1_right_margin_avg - array2_left_margin_avg)
    print("diff:", diff)
    return array1_right_margin_avg, array2_left_margin_avg, diff
array1_right_margin_avg, array2_left_margin_avg, diff = margins(array1, array2)

def level_out_arrays(array1, array2, array1_avg, array2_avg):
    print_diagnostics(array1, array2)
    diff = abs(array1_avg - array2_avg)
    if array1_avg > array2_avg:
        array2 += diff
    else:
        array1 += diff

level_out_arrays(array1, array2, array1_right_margin_avg, array2_left_margin_avg)
margins(array1, array2)
print_diagnostics(array1, array2)

# array1 = min_max_scale(array1)
# array2 = min_max_scale(array2)

margins(array1, array2)
print_diagnostics(array1, array2)

# Łączenie sektorów
combined_array = np.hstack((array1, array2))
combined_array = min_max_scale(combined_array)

# Zapis jako PNG
image = Image.fromarray(combined_array)
image.save("combined_map_hard_scaled.png")

print("Eksport zakończony: combined_map_hard_scaled.png")
