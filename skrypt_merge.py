from osgeo import gdal
import numpy as np
from PIL import Image

# Ścieżki do plików .asc
sektor1_path = "dabrowa_lewo.asc"  # sektor po lewej
sektor2_path = "wk_prawo.asc"  # sektor po prawej

# Wczytanie plików .asc
sektor1 = gdal.Open(sektor1_path)
sektor2 = gdal.Open(sektor2_path)

# Odczyt danych jako tablic NumPy
array1 = sektor1.ReadAsArray()
array2 = sektor2.ReadAsArray()

# Przytnij do najmniejszego rozmiaru
def cut_to_min_size(array1, array2):
    min_rows = min(array1.shape[0], array2.shape[0])
    min_cols = min(array1.shape[1], array2.shape[1])
    array1 = array1[:min_rows, :min_cols]
    array2 = array2[:min_rows, :min_cols]
    return array1, array2

array1, array2 = cut_to_min_size(array1, array2)

# Normalizacja sektorów do wspólnego zakresu (0–255)
def normalize(array):
    min_val = np.min(array)
    max_val = np.max(array)
    return ((array - min_val) / (max_val - min_val) * 255).astype(np.uint8)

normalized_array1 = normalize(array1)
normalized_array2 = normalize(array2)

# Połączenie sektorów (sektor1 po lewej, sektor2 po prawej)
combined_array = np.hstack((normalized_array1, normalized_array2))

# Zapis do pliku PNG
image = Image.fromarray(combined_array)
image.save("combined_map_new.png")

print("Eksport zakończony: combined_map_new.png")
