# Yagami maketi — final4

Bu set, 22 Eylül 2026 tarihinde verilen **izometrik referansa** göre hazırlanmıştır. Eski `final3` setinden farklıdır: bitkiler yoktur; dört fener, iki sıra halinde sekiz fıçı, üç spot, ayrı YAGAMI tabelası, dalgalı perde ve iki paspas vardır.

## Dosyalar

- `japan_shop_final.blend`: dokuları dosyaya gömülü, parçaları ayrı düzenlenebilir sahne.
- `stl_baski/`: 26 parçanın her biri XY merkezine ve Z=0 seviyesine taşınmıştır. Dilimleyicide tek tek baskı hazırlamak için kullanın.
- `stl_montaj/`: aynı 26 parça, ortak montaj koordinatlarıyla. Bütün dosyaları birlikte içe aktarırken otomatik merkezlemeyi kapatın.
- `parcalar.json`: her parçanın ölçüsü, montaj sınırları ve baskı kopyasına uygulanan öteleme.
- `izometrik.png`, `on.png`, `arka.png`: teslim edilen sahneden alınan dokulu görünümler.
- `mesh_kontrol.png`: aynı geometrinin dokusuz görünümü. Baskıda gerçekten bulunan kabartmaları gösterir.
- `parca_katalogu.png`: parçaların tek tek görünümü.

**Birim:** milimetre. **Toplam dış ölçü:** yaklaşık 243,48 × 130,43 × 240 mm. +X sağ, -Y ön cephe, +Z yukarı.

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

Önce taban ve eşiği, ardından binayı yerleştirin. 26 numaralı desteği tabela arkasına yerleştirin; perde, tabela, fenerler ve spotlarla devam edin. Fıçıları iki sıra dörderli dizin. Son olarak menü, paspaslar, küp tabela ve yol babasını yerleştirin. Parçalar yapıştırmalı montaj içindir; geçmeli pim veya kilit sistemi yoktur. Sahnede temas için bazı parçalar az miktarda iç içe geçer; birleşik tek gövde STL olarak değerlendirmeyin.

## Baskı ve görünüm notları

STL renk veya resim dokusu taşımaz. Yazı/desenlerin bir kısmı kabartmadır; mozaik renkleri, ince ahşap damarları ve bazı fener süsleri dokudadır. Bu ayrımı `mesh_kontrol.png` üzerinde görebilirsiniz. Dokulu görünüm Blender dosyasındadır.

Bu bir dış cephe maketidir. Cam kapılar kapalı katı yüzey olarak modellenmiştir; iç mekândaki sandalye, masa ve insan figürleri modellenmemiştir. Küçük menü ve küp tabela grafikleri sadeleştirilmiştir. Fıçılar üç dekor çeşidi kullanır; referanstaki sekiz etiketin birebir kopyası değildir. Çalışma fotoğraftan türetilmiş bir yorumdur, ölçülü mimari tarama değildir.

Parçaların Z=0 üzerinde bulunması, desteksiz basılacakları anlamına gelmez. Özellikle fenerler, saçak, yazı kabartmaları ve menü tablası için yazıcınıza göre yönlendirme ve destek hazırlayın. Bu teslimatta fiziksel baskı denemesi yapılmadı.

## Geometri kontrolleri

Kontrol, teslim edilen STL dosyalarının kendisi üzerinde yapılır: kapalı yüzey, tek bağlı gövde, tutarlı yüz yönü, pozitif hacim, açık veya çoklu kenar, sıfır alanlı/yinelenen yüz ve yüzeylerin kendi içinde kesişmesi. Blender sahnesi ayrıca STL üçgenleriyle karşılaştırılır. Sayısal sonuçlar `kontrol_raporu.json` ve `sahne_kontrolu.json` dosyalarındadır.
