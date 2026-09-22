# Referanstan yeniden oluşturma

Ana kaynak `references/master.png` dosyasıdır. Gerçek mekân fotoğrafı `references/real_detail.png` ayrıntı kaynağı olarak kullanılmıştır. Diğer referans görselleri, binaya aksesuar kaynaşmasını önlemek için tek nesne halinde hazırlanmıştır.

Meshy 7.1 ile bina, taban, tabela, dört fener ve fıçı çeşitleri üretilmiştir. İlk fıçının biçimi teslimat için uygun bulunmadı; son grupta sonraki üç çeşit kullanıldı. Toplam 11 üretim 385 kredi tüketti; son bakiye 1855 kredi. API ile onarım veya tekrar dokulama ücreti oluşmadı. Anahtar depoya kaydedilmemiştir.

## İş akışı

1. `prepare_request.py`: izole görselden üretim isteği hazırlar. API çağrısı için anahtar ayrı, geçici bir oturumda tutulur; bu betik anahtar okumaz veya kaydetmez.
2. `download_assets.py`: tamamlanan görevlerin GLB ve STL dosyalarını indirir. Ham yanıtlar ve dosyalar `raw/` altında yerel olarak tutulur; depoya alınmaz.
3. `repair_meshes.py`: mikroskobik kopuk parçaları ayıklar, küçük açıklıkları ve kesişmeleri yerel olarak onarır. İsteğe bağlı varlık adları yalnızca seçilen kaynakları işler.
4. `refine_building.py`: üst pencere açıklıklarını düzeltir, saçak kaplamasına fiziksel dikey derzler ekler. Mozaik ve ahşap renk ayrıntıları dokuda kalır.
5. `transfer_uv.py`: onarılan üçgenlere özgün doku koordinatlarını taşır.
6. `accessories.py`: eşik, perde, küp tabela, spotlar, menü, paspaslar, yol babası ve montaj desteğini kapalı katı geometri olarak üretir.
7. `assemble.py`: dokuları aktarır, dört fener ve sekiz fıçı dahil 26 parçayı yerleştirir; yüksekliği 240 mm'ye ölçekler; iki STL dizisini ve Blender sahnesini çıkarır. Ana renk dokuları 2048, normal dokuları 1024, yardımcı yüzey dokuları 512 piksele indirilerek dosyaya gömülür. Orijinal 4K kaynaklar yerelde korunur.
8. `validate_final.py` ve `verify_scene.py`: son STL dosyalarını ve sahneyle eşleşmesini doğrular.
9. `catalog.py`: kayıtlı sahneyi değiştirmeden parça kataloğunu görüntüler.

Son üç betik ve son dosyaların kontrolü dışında yeniden üretim, depoya dahil edilmeyen ham GLB/STL dosyalarını gerektirir. Oluşturma için Blender 5.2.1 ve `requirements.txt` içindeki Python paketleri kullanılmıştır.

Sınırlar: dış cephe maketi; iç mekân yoktur, küçük grafikler sadeleştirilmiştir. Sayısal mesh kontrolleri fiziksel baskı denemesinin yerine geçmez. Ayrıntılı kapsam `final4/OKU_BENI.md` dosyasındadır.
