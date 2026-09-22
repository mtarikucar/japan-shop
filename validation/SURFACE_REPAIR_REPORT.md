# Yüzey onarımı — 22 Eylül 2026

Kaynak: GitHub `main` dalındaki `ae6af10501b88c615b14412c4fdae1557a464268`. Önceki 12 STL, ön/arka/yan renderları ve topoloji ölçümleriyle ayrı ayrı incelendi.

## Sorunun nedeni

Önceki doğrulama yüzeylerin kapalı, yönlerinin tutarlı ve tek gövde olmasını kontrol ediyordu. Bu koşullar, geometrik olarak çökmüş veya sivrilmiş bir yüzeyin düzgün olduğunu göstermez. Bina, ışıklı tabela, menü standı ve sarı baba bu kontrolleri geçtiği halde bozuk yüzeyler içeriyordu. Ayrıca bitkilerde yüzey kesişmesi kontrolü yapılmamıştı: bambuda 51.524, akçaağaçta 24.691 yüz kesişme seçimine girdi.

Yeni kontrol, dışa aktarılmış STL dosyalarını tekrar okuyup PyMeshLab ile yüzey kesişmelerini de tarar. [Filtre açıklaması](https://pymeshlab.readthedocs.io/en/latest/filter_list.html#compute-selection-by-self-intersections-per-face).

## Parça bazında işlemler

| STL | İnceleme ve işlem |
| --- | --- |
| 01_tabla | Düz yüzeyler ve topoloji sağlam; dosya değiştirilmedi. |
| 02_bina | Yan/arka duvarlar, çatı, saçak, pencere yüzeyleri, kapı panelleri ve alt kenar yeniden kuruldu. Sivri yan uzantılar ve eğri alt çıkıntı temizlendi. Duvar derzleri düzenlendi. Pencere yerleşimi, kabartmalı ana tabela ve kapı kolları korundu; pencere çerçeveleri ve cam panelleri düzleştirildi. |
| 03_ficilar | Ön/arka/yan yüzeyler ve kesişme testi kontrol edildi. Kabartmalar ve kapak bağları korundu; dosya değiştirilmedi. |
| 03_ficilar_ust | Alt fıçı seti gibi kontrol edildi; dosya değiştirilmedi. |
| 04_sol_saksi_bambu | Kesişen yüzeyler 0,12 mm voxel ile yeniden oluşturuldu. Küçük kopuk parçalar temizlendi; topoloji korunarak 850.000 üçgene indirildi. |
| 05_sag_saksi_akcaagac | Aynı hacimsel onarım uygulandı; 850.000 üçgen, sıfır kesişen yüz. |
| 06_fener_sol_1 | Gövdedeki düzensiz katlanmalar yerine kaynak modelin medyan yarıçap profili kullanıldı. Halkalı gövde biçimi ve üst askı korundu. |
| 07_fener_sol_2 | Aynı yöntemle gövde düzeltildi; üst askı korundu. |
| 08_fener_sag | Görünüş ve topoloji uygun; dosya değiştirilmedi. |
| 09_isikli_tabela | Çökmüş köşe ve düzensiz kenarlar yerine düz kutu yüzeyleri oluşturuldu. Alt montaj ayağı korundu. |
| 10_menu_standi | Eğri ve katlanmış menü tablası düz, çerçeveli ve bölmeli bir panelle değiştirildi. Eğimi ve ana direği korundu; arkadaki bozuk ikincil yapı sadeleştirildi. |
| 11_baba_sari | Katlanmış ön/arka yüzler temiz bir kemer gövdesiyle değiştirildi. Dış ölçüler, merkez deliği ve iki yatay girinti korundu. |

## Ölçü ve ayrıntı değişiklikleri

Modeller ölçeklenmedi ve ortak montaj koordinatları korundu. Ancak bozuk uzantıların kaldırılması ve yüzeylerin yeniden kurulması bazı dış ölçüleri değiştirdi:

- Bina: **227,757 × 84,549 × 222,034 → 219,696 × 73,000 × 222,000 mm**. Üst kot 240 mm, alt kot 18 mm. Düzleştirilen yüzeylerde eski düzensiz taş/üçgen dokusu sadeleştirildi.
- Menü standı: **24,798 × 20,459 × 55,674 → 24,000 × 17,449 × 55,354 mm**. Eski çift/bozuk panel yapısı daha sade tek panel oldu.
- Fenerlerin halka derinliği ve çok küçük gövde düzensizlikleri değişti. Sarı babanın dış ölçüleri korundu; yüzeyindeki eski bozuk kabartı kaldırıldı.
- Bitkilerde ince yaprak uçları ve küçük kopuk artıklar değişebilir. İki yönde 3.000'er yüzey örneğiyle ölçülen sapmanın %95 değeri bambuda **0,045 mm**, akçaağaçta **0,035 mm**. Örneklerdeki en büyük mesafe sırasıyla 1,695 ve 0,402 mm; bunlar tam yüzey için maksimum hata garantisi değildir. Sonuçlar `plant_surface_distance.json` içindedir.

Tüm güncel ölçüler: [BOYUTLAR.txt](../final3/BOYUTLAR.txt).

## Doğrulama

12/12 STL: tek bağlı bileşen, kapalı yüzey, tutarlı yüz yönleri, pozitif hacim; sıfır açık kenar, sıfır manifold olmayan kenar, sıfır sıfır-alanlı üçgen ve **sıfır kesişen yüz**. Yeni kesişme kontrolü onarım öncesinde bambu dosyasında başarısız oldu; onarım sonrasında bütün dosyalar geçti. Sayısal sonuçlar `after.json`; bu turun başlangıç ölçümleri `surface_before.json` içindedir.

Blender sahnesindeki 12 mesh, üçgen koordinatları üzerinden STL dosyalarıyla birebir karşılaştırıldı (`scene_check.json`). Her parçanın ön/arka/yan görünüşü tekrar incelendi. [Ön](previews/front.jpg), [arka](previews/back.jpg), [yan](previews/side.jpg), [binada önce/sonra](previews/building_comparison.jpg).

Bu çalışma dijital geometri ve görsel yüzey kontrolüdür. Fiziksel baskı, minimum et kalınlığı, mekanik geçme toleransı ve parçalar arası çakışma analizi yapılmadı.

## Tekrar çalıştırma

```sh
python -m pip install -r validation/requirements.txt
python validation/validate_meshes.py
```

Onarım betikleri **ae6af10 kaynak STL seti** için yazıldı; düzeltilmiş dosyalar üzerine tekrar uygulanmamalıdır. Kaynak STL'leri ayrı bir klasöre çıkarın:

```sh
git archive ae6af10 final3 | tar -x -C /path/to/source
python validation/repair_surface_models.py /path/to/source/final3 /path/to/output
blender -b --python validation/remesh_plants.py -- /path/to/source/final3 /path/to/voxel
python validation/clean_plant.py /path/to/voxel/04_sol_saksi_bambu.stl /path/to/output/04_sol_saksi_bambu.stl
python validation/clean_plant.py /path/to/voxel/05_sag_saksi_akcaagac.stl /path/to/output/05_sag_saksi_akcaagac.stl
```

Değiştirilmeyen dört STL kaynak setten korunur. `build_preview.py`, güncel `final3/*.stl` dosyalarından Blender sahnesini ve montaj önizlemelerini oluşturur. Blender 5.2.1 kullanıldı.
