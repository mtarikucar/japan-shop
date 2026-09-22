# Japan Shop

Japon dükkânı maketinin onarılmış 12 STL parçası `final3/` klasöründedir. Birimler milimetre; toplam yükseklik yaklaşık 240 mm. +X sağ, -Y ön cephe, +Z yukarı.

- [Blender dosyası](final3/japan_shop_repaired.blend)
- [Ölçüler](final3/BOYUTLAR.txt)
- [Güncel yüzey onarımı ve kontrol raporu](validation/SURFACE_REPAIR_REPORT.md)
- [Tüm parçaların önizlemesi](validation/previews/front.jpg)
- [Bina: önce / sonra](validation/previews/building_comparison.jpg)

## Güncel STL önizlemesi

Bunlar onarılmış geometriden Blender'da alınan görüntülerdir. Renkler parçaları ayırt etmek içindir; STL dosyaları doku içermez.

![Onarılmış model](final3/onarilmis_on.png)
![Arka görünüm](final3/onarilmis_arka.png)
![Yeniden oluşturulan tabla](final3/onarilmis_tabla.png)

Önceki dokulu referans görselleri `birlesik_34.png`, `birlesik_on.png` ve `menu_yakin.png` adlarıyla korunmuştur. Eski STL sürümü Git geçmişindeki `39bd9b4` commit'indedir.

## Kontrolü tekrar çalıştırma

Kapalı yüzey, tek gövde, yüz yönleri ve yüzey kesişmeleri kontrol edilir:

```sh
python -m pip install -r validation/requirements.txt
python validation/validate_meshes.py
```

22 Eylül yüzey onarımında 12 parça ayrı ayrı incelendi; 8 parça düzeltildi. Bozuk yüzeyleri yeniden kurulan bina ve menü standının ölçüleri değişti; güncel ölçüler ve ayrıntı değişiklikleri rapordadır. Önceki onarılmış sürüm `ae6af10` commit’indedir.
