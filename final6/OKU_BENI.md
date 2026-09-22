# Yagami maketi — final6

Bu set `final5` ile aynıdır; tek fark, 22 cm'lik baskı alanına sığması için binanın (`02_bina`) pencereli üst katının **24 mm kısaltılmasıdır**. Toplam yükseklik 240 mm'den **216 mm**'ye indi. Diğer 27 parça final5 ile bayt bayt aynıdır.

## Dosyalar

- `japan_shop_final.blend`: dokuları dosyaya gömülü, parçaları ayrı düzenlenebilir sahne. Dosya büyük olduğu için Git deposunda yoktur.
- `stl_baski/`: 28 parçanın her biri XY merkezine ve Z=0 seviyesine taşınmıştır. Dilimleyicide tek tek baskı hazırlamak için kullanın.
- `stl_montaj/`: aynı 28 parça, ortak montaj koordinatlarıyla. Bütün dosyaları birlikte içe aktarırken otomatik merkezlemeyi kapatın.
- `parcalar.json`: her parçanın ölçüsü, montaj sınırları ve baskı kopyasına uygulanan öteleme. `02_bina` kaydında kısaltmada kullanılan Z eşlemesi de vardır.
- `izometrik.png`, `on.png`, `arka.png`: sahneden alınan dokulu görünümler.
- `mesh_kontrol.png`: aynı geometrinin dokusuz görünümü. Baskıda gerçekten bulunan kabartmaları gösterir.
- `parca_katalogu.png`: parçaların tek tek görünümü.

**Birim:** milimetre. **Toplam dış ölçü:** yaklaşık 244,56 × 130,43 × 216,00 mm. +X sağ, -Y ön cephe, +Z yukarı. **Bina tek başına:** 182,61 × 60,87 × 193,39 mm (final5'te 217,39 mm).

## Üst katın kısaltılması

Saçağın üstünden çatıya kadar olan pencereli kat (Z 198,9–240) yalnızca yaklaşık 41 mm yüksekliğindedir. Buradan tek parça halinde 24 mm kesilseydi pencere denizlikleri ya da çatı kenarı kaybolurdu. Bu yüzden 24 mm, kesiti dört cephede de değişmeyen düz bantlardan alındı:

| Final5'te Z (mm) | Bölge | Yükseklik |
|---|---|---|
| 198,9–213,3 | Denizlik altındaki düz duvar | 14,4 → 1,8 |
| 213,3–219,9 | Denizlik ve alt pencere kasası | 6,6 → 5,4 |
| 219,9–228,5 | Pencere camı | 8,6 → 1,6 |
| 228,5–231,5 | Yan/arka korniş, cam | 3,0 → 2,4 |
| 231,5–234,5 | Pencere camı | 3,0 → 0,4 |
| 234,5–240,0 | Çatı kenarı, üst kasa, parapet | 5,5 → 5,5 (yalnızca aşağı kaydırıldı) |

Saçak, cephe, tabelalar ve Z 198,9 altındaki her şey değişmedi. Pencereler, denizlikler, dikey kayıtlar ve çatı parapeti korunur; pencere camları kısalır. Yalnızca Z koordinatları tek yönlü artan bir eşlemeyle taşındığı için üçgen yapısı ve doku koordinatları bozulmadı. Mozaik süs ve cam dokusu Blender sahnesinde dikeyde sıkışmış görünür; bu yalnızca dokudur, STL'yi etkilemez.

## Parçalar ve montaj

| Numaralar | İçerik |
|---|---|
| 01–05 | Taban, bina, eşik, ana tabela, dalga desenli perde |
| 06–09 | Dört farklı fener |
| 10 | Kabartma yazılı küp tabela |
| 11–13 | Üç spot |
| 14 | Menü standı; tabla, ayak ve kaide tek gövdedir |
| 15–18 | Alt sıradaki dört fıçı |
| 19–22 | Üst sıradaki dört fıçı |
| 23–24 | Eşik ve kaldırım paspasları |
| 25 | Delikli sarı yol babası |
| 26 | Tabela ve fenerlerin arkasındaki montaj desteği |
| 27 | Önceki STL setinden sol bambu saksısı |
| 28 | Önceki STL setinden sağ akçaağaç saksısı |

Montaj sırası final5 ile aynıdır: önce taban ve eşik, ardından bina. 26 numaralı desteği tabela arkasına yerleştirin; perde, tabela, fenerler ve spotlarla devam edin. Fıçıları iki sıra dörderli dizin. Son olarak menü, paspaslar, küp tabela ve yol babasını yerleştirin. Parçalar yapıştırmalı montaj içindir; geçmeli pim veya kilit sistemi yoktur.

## Baskı ve görünüm notları

STL renk veya resim dokusu taşımaz. Yazı ve desenlerin bir kısmı kabartmadır; mozaik renkleri, ince ahşap damarları ve bazı fener süsleri yalnızca dokudadır (`mesh_kontrol.png`). Bu bir dış cephe maketidir; iç mekân modellenmemiştir.

Parçaların Z=0 üzerinde bulunması, desteksiz basılacakları anlamına gelmez. Fenerler, saçak, yazı kabartmaları ve menü tablası için yazıcınıza göre yönlendirme ve destek hazırlayın. Bu sürüm yalnızca yüksekliği değiştirir: taban (`01_tabla`) hâlâ 243,5 × 130,4 mm'dir ve 220 × 220 mm'lik bir tablaya hiçbir açıyla sığmaz. Bu teslimatta fiziksel baskı denemesi yapılmadı.

## Geometri kontrolleri

Final5'teki kontrollerin tümü final6 dosyaları üzerinde yeniden çalıştırıldı:

- 28 montaj STL'si ve 28 baskı kopyası: tek bağlı gövde, kapalı yüzey, tutarlı yüz yönü, pozitif hacim; açık/çoklu kenar, dejenere/yinelenen yüz ve kendi içinde yüzey kesişmesi yok (`kontrol_raporu.json`).
- Parçalar arası katı kesişim hacmi 0,005 mm³ altında (`parcalar_arasi_kontrol.json`).
- Gerekli 27 bağlantının her birinde 0,025 mm içinde en az üç temas örneği var; temas sayıları final5 ile aynı (`temas_olcumleri.json`).
- Blender sahnesindeki geometri STL üçgenleriyle birebir eşleşiyor (`sahne_kontrolu.json`).

Önceki sürümdeki oturma düzeltmeleri için [`../final5/YERLESIM_DUZELTMELERI.md`](../final5/YERLESIM_DUZELTMELERI.md) dosyasına bakın.
