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

## final5: oturmaların düzeltilmesi ve eski saksılar

Bu aşamada yeni API üretimi yapılmaz. `final3` saksıları ve `final4` parçaları kullanılır:

1. `blender -b final4/japan_shop_final.blend --python rebuild_v2/scripts/extract_fit_uv.py`
2. `python rebuild_v2/scripts/fit_assembly.py`
3. `python rebuild_v2/scripts/fit_cube_seat.py`
4. `python rebuild_v2/scripts/clear_barrel_jamb.py`
5. `blender -b final4/japan_shop_final.blend --python rebuild_v2/scripts/assemble_fitted.py`
6. `python rebuild_v2/scripts/validate_final.py final5`
7. `python rebuild_v2/scripts/check_assembly_solids.py`
8. `python rebuild_v2/scripts/check_contacts.py final5/stl_montaj final5/temas_olcumleri.json`
9. `blender -b final5/japan_shop_final.blend --python rebuild_v2/scripts/verify_scene.py`
10. Kayıtlı final5 sahnesiyle `render_scene.py` ve `catalog.py` çalıştırılır; `python rebuild_v2/scripts/package.py final5` paketi doğrulayarak çıkarır.

Geçici UV verileri `fit_cache/` altında yerelde tutulur. Büyük Blender dosyası GitHub sürüm ZIP'inde bulunur; tek dosya boyutu nedeniyle Git deposuna ayrıca eklenmez. Tüm STL parçaları depodadır.

Kontrol, parça başına sağlam mesh yanında gerçek katıların kesişim hacmini ve gerekli bağlantılardaki temas örneklerini de kapsar. Dışa aktarım sırasında birleşim kenarlarındaki 0,0001 mm'den yakın noktalar gerektiğinde birleştirilir. İşaretli ışın mesafeleri kıvrımlı/çıkıntılı yüzeylerde tek başına kesişme ölçüsü değildir; katı kesişim kontrolü ayrıca yapılır.

## final6: pencereli üst katın 24 mm kısaltılması

Yeni üretim yapılmaz; final5 dosyaları kullanılır. Pencere katı (Z 198,9–240) yalnızca ~41 mm olduğu için 24 mm tek parça kesilmez. Kesiti dört cephede değişmeyen bantlardan (denizlik altı duvar, pencere camı) alınır; denizlik/kasa ve korniş bantları hafifçe kısalır, çatı kenarı yalnızca aşağı kayar. Yalnızca Z koordinatı tek yönlü artan bir eşlemeyle taşınır; üçgen yapısı ve UV'ler değişmez. Eşleme `shorten_upper_floor.py` içindeki `KNOTS` tablosundadır.

1. `python rebuild_v2/scripts/shorten_upper_floor.py`
2. `blender -b final5/japan_shop_final.blend --python rebuild_v2/scripts/shorten_scene.py`
3. `python rebuild_v2/scripts/validate_final.py final6`
4. `python rebuild_v2/scripts/check_assembly_solids.py final6`
5. `python rebuild_v2/scripts/check_contacts.py final6/stl_montaj final6/temas_olcumleri.json`
6. `blender -b final6/japan_shop_final.blend --python rebuild_v2/scripts/verify_scene.py`
7. Kayıtlı final6 sahnesiyle `render_scene.py` ve `catalog.py` çalıştırılır; `python rebuild_v2/scripts/package.py final6` hash listesini ve yerel ZIP paketini çıkarır.
