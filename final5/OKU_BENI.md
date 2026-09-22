# Yagami maketi — final5

Bu set, 22 Eylül 2026 tarihinde verilen **izometrik referansa** göre hazırlanmıştır. Eski `final3` setindeki bambu ve akçaağaç saksıları yanlara geri eklenmiştir; dört fener, iki sıra halinde sekiz fıçı, üç spot, ayrı YAGAMI tabelası, dalgalı perde ve iki paspas vardır.

## Dosyalar

- `japan_shop_final.blend`: dokuları dosyaya gömülü, parçaları ayrı düzenlenebilir sahne.
- `stl_baski/`: 28 parçanın her biri XY merkezine ve Z=0 seviyesine taşınmıştır. Dilimleyicide tek tek baskı hazırlamak için kullanın.
- `stl_montaj/`: aynı 28 parça, ortak montaj koordinatlarıyla. Bütün dosyaları birlikte içe aktarırken otomatik merkezlemeyi kapatın.
- `parcalar.json`: her parçanın ölçüsü, montaj sınırları ve baskı kopyasına uygulanan öteleme.
- `izometrik.png`, `on.png`, `arka.png`: teslim edilen sahneden alınan dokulu görünümler.
- `mesh_kontrol.png`: aynı geometrinin dokusuz görünümü. Baskıda gerçekten bulunan kabartmaları gösterir.
- `parca_katalogu.png`: parçaların tek tek görünümü.

**Birim:** milimetre. **Toplam dış ölçü:** yaklaşık 244,56 × 130,43 × 240,00 mm. +X sağ, -Y ön cephe, +Z yukarı.

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

Önce taban ve eşiği, ardından binayı yerleştirin. 26 numaralı desteği tabela arkasına yerleştirin; perde, tabela, fenerler ve spotlarla devam edin. Fıçıları iki sıra dörderli dizin. Son olarak menü, paspaslar, küp tabela ve yol babasını yerleştirin. Parçalar yapıştırmalı montaj içindir; geçmeli pim veya kilit sistemi yoktur. Parçalar ayrı basılır; montaj yüzeyleri birbirine uyarlanmıştır. Geçmeli kilit veya baskı toleransı verilmiş mekanik pim sistemi değildir.

## Baskı ve görünüm notları

STL renk veya resim dokusu taşımaz. Yazı/desenlerin bir kısmı kabartmadır; mozaik renkleri, ince ahşap damarları ve bazı fener süsleri dokudadır. Bu ayrımı `mesh_kontrol.png` üzerinde görebilirsiniz. Dokulu görünüm Blender dosyasındadır.

Bu bir dış cephe maketidir. Cam kapılar kapalı katı yüzey olarak modellenmiştir; iç mekândaki sandalye, masa ve insan figürleri modellenmemiştir. Küçük menü ve küp tabela grafikleri sadeleştirilmiştir. Fıçılar üç dekor çeşidi kullanır; referanstaki sekiz etiketin birebir kopyası değildir. Çalışma fotoğraftan türetilmiş bir yorumdur, ölçülü mimari tarama değildir.

Parçaların Z=0 üzerinde bulunması, desteksiz basılacakları anlamına gelmez. Özellikle fenerler, saçak, yazı kabartmaları ve menü tablası için yazıcınıza göre yönlendirme ve destek hazırlayın. Bu teslimatta fiziksel baskı denemesi yapılmadı.

## Geometri kontrolleri

Kontrol, teslim edilen STL dosyalarının kendisi üzerinde yapılır: kapalı yüzey, tek bağlı gövde, tutarlı yüz yönü, pozitif hacim, açık veya çoklu kenar, sıfır alanlı/yinelenen yüz ve yüzeylerin kendi içinde kesişmesi. Blender sahnesi ayrıca STL üçgenleriyle karşılaştırılır. Sayısal sonuçlar `kontrol_raporu.json` ve `sahne_kontrolu.json` dosyalarındadır.

## Bu sürümde düzeltilen oturmalar

- Binanın altı, eşiğe tam basan bir yüzeye tamamlandı; eşik altı kaldırıma uyarlandı.
- Alt ve üst fıçıların gizli oturma yüzeyleri düzleştirildi; üst sıra için düz destek alanları eklendi. Fıçı grubu kapı direğinden, paspas da fıçıdan ayrıldı.
- Fenerler ahşap çerçeveden öne alındı. 26 numaralı arka desteğin temasları bina, tabela ve fenerlerin gerçek yüzeylerine göre şekillendirildi.
- Spotların tavan plakaları saçak eğimine, küp tabelanın gizli montaj çıkıntısı binanın yan yüzeyine uyarlandı.
- Yol babası kaldırıma gömülmek yerine yol yüzeyine oturtuldu. Kaldırım paspasının altı zemine uyarlandı.
- Saksıların eski bitki geometrileri korundu. Sol saksı 0,65; sağ saksı 0,48 oranında her eksende eşit ölçeklendi. Altlarına zemine uyan oturma yüzeyleri eklendi.

`temas_olcumleri.json` gerçek yüzeyler üzerinde 0,025 mm toleranslı temas örneklerini kaydeder. Eğri/çıkıntılı yüzeylerde aynı ışının birden fazla yüzeyi kesmesi nedeniyle işaretli ışın farkı tek başına hacim çakışması değildir. `parcalar_arasi_kontrol.json` ayrıca gerçek katı kesişim hacmini ölçer; 0,005 mm³ altı sayısal kırıntılar tolerans içinde kabul edilir.

Bu düzeltmede yeni Meshy üretimi veya API kredisi kullanılmadı.
