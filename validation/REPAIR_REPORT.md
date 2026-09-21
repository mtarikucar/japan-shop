# Onarım raporu — 21 Eylül 2026

Kaynak: `39bd9b4` commit'indeki 12 STL. İşlem: Blender 5.1.2 ile içe aktarma, yinelenen/bozuk geometri temizliği, normal yönleri, tabla modelleme, bitkilerde 0.18 mm voxel remesh ve önizleme; PyMeshFix ile delik/yüzey onarımı; Manifold ile bina üzerindeki katı işlemleri.

## Yapılan değişiklikler

- **Tabla:** sivri üçgenler, açık yan yüzeyler ve bozuk üst yüzey nedeniyle yeniden modellendi. 260.432 × 145.340 mm dış genişlik/derinlik korundu. Üst seviye 18 mm, yol 8.21 mm; basamak Y=-54 mm. Küçük kenar pahları eklendi. Eski düzensiz taş çizgileri ve köşe şekilleri sadeleştirildi; bozuk 22.53 mm çıkıntılar kaldırıldı.
- **Bina:** bağımsız bitki kırıntıları ve cephe dışındaki bitki kalıntıları temizlendi; açık yüzeyler kapatıldı. Hasarlı kapı alanı iki düz panel, çerçeve ve iki tutamakla yeniden kuruldu. Kabartmalı tabelaya duvara bağlanan gizli destekler eklendi. Sonuç tek bağlı gövde. Orijinal cephe/tuğla yüzeyinin düşük poligonlu karakteri korunuyor; bu bir yüksek detaylı yeniden modelleme değildir.
- **Bambu ve akçaağaç:** ana saksı/bitki gövdesi korunarak hacimsel onarım uygulandı. Havada kalan bağımsız yaprak parçaları kaldırıldı. Özellikle bambunun kopuk tepe yaprakları çıkarıldığından bitki yüksekliği azaldı; voxel işleminden dolayı çok ince ayrıntılar değişebilir.
- **Fıçılar, fenerler, ışıklı tabela, menü standı ve sarı baba:** küçük kopuk kırıntılar temizlendi, delikler onarıldı ve normal yönleri düzeltildi.
- **Yerleşim:** saksılar, alt fıçılar ve menü ayağı 18 mm tabla üstüne oturtuldu; üst fıçılar aynı düşey farkla taşındı. Diğer parçalar ortak montaj koordinatlarında tutuldu.

## Doğrulama

Dışa aktarılan STL'ler tekrar okunarak 12/12 dosyada şu koşullar doğrulandı: tek bağlı bileşen, kapalı yüzey, tutarlı yüz yönleri, pozitif hacim, sıfır açık kenar, sıfır ikiden fazla yüzün paylaştığı kenar ve sıfır sıfır-alanlı üçgen. Sayısal sonuçlar `after.json`, kaynak ölçümleri `before.json` dosyalarındadır. Ön/arka görünüm, yalnız bina ve yalnız tabla Blender renderları görsel olarak kontrol edildi.

Bu kontroller fiziksel baskı denemesi, minimum et kalınlığı analizi veya parçalar arası çakışmazlık garantisi değildir. İnce bitki detayları için yazıcıya uygun destek ve baskı ayarları ayrıca seçilmelidir. Parçalar montaj koordinatlarında olduğu için ayrı ayrı dilimlenirken baskı tablasına yerleştirilmelidir.
