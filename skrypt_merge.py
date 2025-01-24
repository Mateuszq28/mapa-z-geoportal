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

# Diagnostyka - zakresy danych
print("Sektor 1 - min:", np.min(array1), "max:", np.max(array1))
print("Sektor 2 - min:", np.min(array2), "max:", np.max(array2))

# Diagnostyka - zakresy danych
print("Po odrzuceniu -9999:")
print("Sektor 1 - min:", np.min(array1[array1 > -9999]), "max:", np.max(array1[array1 > -9999]))
print("Sektor 2 - min:", np.min(array2[array2 > -9999]), "max:", np.max(array2[array2 > -9999]))

# Zamiana wartości brakujących (-9999) na zero
array1[array1 == -9999] = 0
array2[array2 == -9999] = 0

# Przycinanie sektorów do najmniejszego wspólnego rozmiaru
def cut_to_min_size(array1, array2):
    min_rows = min(array1.shape[0], array2.shape[0])
    min_cols = min(array1.shape[1], array2.shape[1])
    return array1[:min_rows, :min_cols], array2[:min_rows, :min_cols]

array1, array2 = cut_to_min_size(array1, array2)

# Twarde skalowanie wartości (zakres od 0 do 1000)
def hard_scale(array, min_value=0, max_value=1000):
    array = np.clip(array, min_value, max_value)
    scaled_array = ((array - min_value) / (max_value - min_value) * 255).astype(np.uint8)
    return scaled_array

# scaled_array1 = hard_scale(array1)
# scaled_array2 = hard_scale(array2)

def min_max_scale(array, min_value=0, max_value=255):
    array = np.clip(array, min_value, max_value)
    scaled_array = ((array - min(array.flatten())) / (max(array.flatten()) - min(array.flatten())) * 255).astype(np.uint8)
    return scaled_array

scaled_array1 = min_max_scale(array1)
scaled_array2 = min_max_scale(array2)

# Łączenie sektorów
combined_array = np.hstack((scaled_array1, scaled_array2))

# Zapis jako PNG
image = Image.fromarray(combined_array)
image.save("combined_map_hard_scaled.png")

print("Eksport zakończony: combined_map_hard_scaled.png")
