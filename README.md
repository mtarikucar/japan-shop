# Japan Shop — Yagami

Güncel model seti **[final4](final4/OKU_BENI.md)** klasöründedir. Kullanıcının verdiği izometrik referansa göre yeniden hazırlanmış, toplam 24 cm yüksekliğinde ve 26 ayrı parçadan oluşan dış cephe maketidir.

- [Baskı için ayrı STL dosyaları](final4/stl_baski)
- [Montaj koordinatlarında STL dosyaları](final4/stl_montaj)
- [Dokulu Blender sahnesi](final4/japan_shop_final.blend)
- [Montaj ve baskı açıklamaları](final4/OKU_BENI.md)
- [Parça ölçüleri](final4/parcalar.json)
- [Geometri kontrol sonuçları](final4/kontrol_raporu.json)

![Birleşik model](final4/izometrik.png)

![Dokudan bağımsız geometri](final4/mesh_kontrol.png)

STL dosyaları renk/doku içermez. Bina kapalı cephe olarak modellenmiştir; iç mekân mobilyaları dahil değildir. Küçük grafiklerde sadeleştirmeler vardır. Ayrıntılı kapsam ve fiziksel baskı notları [paket açıklamasında](final4/OKU_BENI.md) bulunur.

## Kontrolleri tekrar çalıştırma

```sh
python -m pip install -r rebuild_v2/requirements.txt
python rebuild_v2/scripts/validate_final.py
blender -b final4/japan_shop_final.blend --python rebuild_v2/scripts/verify_scene.py
```

Üretim referansları ve yeniden oluşturma betikleri `rebuild_v2/` altındadır. Ham servis yanıtları, erişim anahtarları ve geçici dosyalar depoya dahil değildir. Önceki `final3` seti geçmiş sürüm olarak korunmuştur.
