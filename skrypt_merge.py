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

# Diagnostyka - wypisanie zakresów danych
print("Sektor 1 - min:", np.min(array1), "max:", np.max(array1))
print("Sektor 2 - min:", np.min(array2), "max:", np.max(array2))

# Zamiana wartości brakujących (jeśli są np. -9999)
array1[array1 == -9999] = np.nan
array1 = np.nan_to_num(array1, nan=np.mean(array1))

array2[array2 == -9999] = np.nan
array2 = np.nan_to_num(array2, nan=np.mean(array2))

# Przycinanie sektorów do najmniejszego wspólnego rozmiaru
def cut_to_min_size(array1, array2):
    min_rows = min(array1.shape[0], array2.shape[0])
    min_cols = min(array1.shape[1], array2.shape[1])
    return array1[:min_rows, :min_cols], array2[:min_rows, :min_cols]

array1, array2 = cut_to_min_size(array1, array2)

# Normalizacja sektorów
def normalize(array):
    min_val = np.min(array)
    max_val = np.max(array)
    if max_val - min_val < 1e-3:  # Wymuszanie minimalnego zakresu
        max_val = min_val + 1
    return ((array - min_val) / (max_val - min_val) * 255).astype(np.uint8)

normalized_array1 = normalize(array1)
normalized_array2 = normalize(array2)

# Połączenie sektorów
combined_array = np.hstack((normalized_array1, normalized_array2))

# Zapis jako PNG
image = Image.fromarray(combined_array)
image.save("combined_map_fixed.png")

print("Eksport zakończony: combined_map_fixed.png")
