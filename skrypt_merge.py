# pip install gdal numpy matplotlib

from osgeo import gdal, gdal_array
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Ścieżki do plików .asc
sektor1_path = "dabrowa_lewo.asc" # sektor po lewej
sektor2_path = "wk_prawo.asc" # sektor po prawej

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

# Sprawdzenie zgodności rozmiarów sektorów
if array1.shape[0] != array2.shape[0]:
    print("shapes", "array1", array1.shape[0], array1.shape[1])
    print("shapes", "array2", array2.shape[0], array2.shape[1])
    raise ValueError("Sektory mają różne liczby wierszy i nie można ich połączyć poziomo.")

# Połączenie sektorów (sektor1 po lewej, sektor2 po prawej)
combined_array = np.hstack((array1, array2))

# Skalowanie wartości do zakresu 0–255
def scale_array(array):
    min_val = np.min(combined_array)
    max_val = np.max(combined_array)
    scaled_array = ((combined_array - min_val) / (max_val - min_val) * 255).astype(np.uint8)
    return scaled_array
combined_array = scale_array(combined_array)

# Zapis do pliku PNG
image = Image.fromarray(combined_array)
image.save("combined_map_new.png")

# Eksport jako PNG (mapa ciepła)
plt.imshow(combined_array, cmap="hot", origin="lower")
plt.colorbar(label="Wysokość")
plt.title("Mapa Ciepła")
plt.savefig("combined_map.png", dpi=300)
plt.close()

# Eksport jako RAW (dla Unreal Engine)
driver = gdal.GetDriverByName("ENVI")
output_dataset = driver.Create("combined_map.raw", combined_array.shape[1], combined_array.shape[0], 1, gdal.GDT_Float32)
output_dataset.GetRasterBand(1).WriteArray(combined_array)
output_dataset.FlushCache()

print("Eksport zakończony: combined_map.png i combined_map.raw")
