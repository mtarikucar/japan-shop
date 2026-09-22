# Yerleşim kontrolü — final5

Önceki kontrolde her parçanın tek başına kapalı ve kesişmesiz olması doğrulanmıştı. Bu, parçaların birbirine doğru oturduğunu garanti etmiyordu. Bu sürümde montaj ayrıca ölçüldü.

## Bulunan ve düzeltilen durumlar

- Bina, eşiğe yalnızca en alttaki birkaç noktadan basıyordu; örneklenen alt yüzeylerde ortanca boşluk yaklaşık 2,13 mm idi. Alt temas yüzeyi tamamlandı.
- Üst fıçılar, alttaki fıçıların ip düğümlerine dayanıyordu. Örneklenen yüzeylerde ortanca açıklık 1,2–1,95 mm aralığındaydı. Gizli birleşme yüzeyleri düzleştirildi, düz destek alanı eklendi.
- Fenerlerin arka desteğinde 0,39–0,68 mm asgari boşluk vardı; diğer bölgelerde fenerler çerçeveye giriyordu. Fenerler öne alındı ve arka destek gerçek yüzeylere göre yeniden oluşturuldu.
- Spot tavan plakaları eğimli saçağa uymuyordu. Plakalar saçak yüzeyine uyarlandı.
- Küp tabelanın montajı gövdenin içine giriyordu. Yan konumu düzeltildi ve gizli, yüzeye uyan montaj çıkıntısı eklendi.
- Sol fıçı grubu kapı direğiyle, son alt fıçı da eşik paspasıyla çakışıyordu. Gerçek katı kesişimleri ölçülerek fıçı grubu ve paspas ayrıldı.
- Kaldırım paspası, eşik altı ve yol babasının zemin ilişkisi düzeltildi.
- `final3/04_sol_saksi_bambu.stl` sola, `final3/05_sag_saksi_akcaagac.stl` sağa eklendi. Tek oranla ölçeklendirilmiş bitkilerin altına zemine uyumlu oturma yüzeyleri yapıldı.

## Son doğrulama

- 28 montaj STL'si ve bunların 28 merkezlenmiş baskı kopyası kontrol edildi.
- Her parça: tek bağlı gövde, kapalı yüzey, tutarlı yüz yönü, pozitif hacim; açık/çoklu kenar, dejenere/yinelenen yüz ve kendi içinde yüzey kesişmesi yok.
- Gerekli 27 bağlantının her birinde, gerçek yüzeyler üzerinde 0,025 mm içinde en az üç temas örneği bulundu.
- Parçalar arası katı kesişim kontrolünde 0,005 mm³ üzerinde istenmeyen çakışma yok.
- Blender geometrisi STL üçgenleriyle ayrıca karşılaştırılır.

Raporlar: `kontrol_raporu.json`, `temas_olcumleri.json`, `parcalar_arasi_kontrol.json`, `sahne_kontrolu.json`.

İşaretli ışın farkları, çok katmanlı/çıkıntılı yüzeylerde doğrudan hacim çakışması anlamına gelmez; katı kesişim raporu bunun için ayrıca üretilmiştir. Parçalar yapıştırmalı montaj içindir. Fiziksel baskı ve yazıcıya özel geçme toleransı testi yapılmamıştır.
