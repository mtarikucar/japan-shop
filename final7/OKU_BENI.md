# Yagami maketi — final7 (eğik reçine baskı için bölünmüş)

Bu set `final6` ile aynı modeldir: toplam yükseklik 216 mm. Fark şu: taban (`01_tabla`) ve bina gövdesi (`02_bina`), reçine yazıcıda eğik basılabilmesi için ikiye bölündü ve yarımlara hizalama pimi eklendi. Diğer 26 parça final6 ile bayt bayt aynıdır. Toplam parça sayısı 30'dur.

![Bölünmüş parçalar](bolunmus_parcalar.png)

## Neden bölündü

Hedef yazıcı ELEGOO Saturn 4 Ultra; baskı hacmi 218,88 × 122,88 × 220 mm. Aşağıdaki kontrolde desteklerin parçayı ~8 mm kaldırdığı ve kenarlarda 2 mm pay bırakıldığı varsayıldı:

| Parça | Ölçü (mm) | 30° eğik | 45° eğik |
|---|---|---|---|
| `01_tabla` (bölünmemiş) | 243,5 × 130,4 × 19,1 | sığmaz | sığmaz (düz de sığmaz) |
| `02_bina` (bölünmemiş) | 182,6 × 60,9 × 193,4 | sığmaz | sığmaz (en fazla ~19°) |
| `01a_tabla_sol` | 121,6 × 130,4 × 19,1 | sığar | sığar |
| `01b_tabla_sag` | 126,8 × 130,4 × 16,5 | sığar | sığar |
| `02a_bina_sol` | 90,0 × 60,9 × 193,4 | sığar | sığar |
| `02b_bina_sag` | 99,6 × 60,9 × 193,4 | sığar | sığar |

Diğer bütün parçalar bölünmeden eğik basılabilir. Bina yarımları için 45° en rahat açıdır; 30°'de parçayı plaka üzerinde biraz döndürmek gerekir. Bina yarımları eğikken yaklaşık 200 mm yer kapladığından her yarım ayrı baskıdır.

## Kesim çizgileri

Kesimler, maketin üzerinde zaten bulunan çizgilere denk getirildi:

| Parça | Kesim | Neden orası |
|---|---|---|
| Bina, saçak altı (Z < 166) | x = −1,3 mm | İki kapı kanadının birleştiği yer, iki kulpun ortası |
| Bina, saçak (Z 166–198,9) | x = −3,3 mm | Saçak tahtaları arasındaki derz |
| Bina, pencere katı (Z > 198,9) | x = −2,0 mm | Sol pencerenin sağ kasasının iç köşesi |
| Taban | x = −0,1 mm | Bordür taşları arasındaki derz |

Bina kesimindeki kademeler saçağın alt ve üst kenarındadır; önden gölgede kalırlar. Kapıda kesim, iki kanadın birleşim çizgisi gibi görünür; kapının üstünde dalga perde, YAGAMI tabelası ve arkasındaki destek (26) birleşimi kapatır. Arka duvarda ve çatıda ince bir birleşim çizgisi kalır; macunla kapatılabilir.

## Hizalama pimleri

- Sağ yarımlarda (`01b`, `02b`) pim, sol yarımlarda (`01a`, `02a`) delik vardır. Binada 5, tabanda 3 pim bulunur.
- Pim Ø4,0 mm, 5 mm boyunda ve ucu 0,5 mm pahlıdır. Delik Ø4,4 mm, 5,5 mm derinliktedir; yarıçapta 0,2 mm, derinlikte 0,5 mm boşluk bırakılmıştır.
- Pim ve delikler iki tarafta da en az 1 mm dolu malzeme içinde kalacak şekilde yerleştirildi.
- Pim sıkı gelirse zımparayla hafifçe inceltin. Yapıştırıcı boşluğu doldurur.

## Baskı notları

- **Yönlendirme:** Kesim yüzeyini (pimli/delikli yüz) plakadan uzağa, yukarıya bakacak şekilde koyun. Pimler plakaya bakarsa destek ister ve kırılabilir. Destekleri görünmeyen yüzlere, yani arka duvara, alt yüze ve kesim yüzüne verin; ön cepheye destek koymayın.
- **İçi boş basım:** Her yarımı ayrı ayrı içi boş yapın. Boşaltma deliklerini kesim yüzüne açın; yapıştırınca kapanır ve görünmez. Deliklerin pim/deliklerden en az 5 mm uzakta olmasına dikkat edin.
- **Reçine:** Bina yarımları dolu halde yaklaşık 769 ml ve 801 ml, taban yarımları yaklaşık 245 ml ve 243 ml hacimdedir. İçi boş basımda bu değerler çok düşer; kesin miktarı dilimleyici gösterir.
- Fiziksel baskı ve pim geçme denemesi yapılmadı.

## Montaj

Önce iki taban yarımını pimleriyle yapıştırın, ardından iki bina yarımını. Kalan montaj final5/final6 ile aynıdır: taban ve eşik, bina, 26 numaralı destek, perde, tabela, fenerler, spotlar, fıçılar; son olarak menü, paspaslar, küp tabela ve yol babası. Eşik (03), perde (05) ve destek (26) iki bina/taban yarımının üzerinden geçer ve birleşimi ayrıca güçlendirir.

## Dosyalar

- `stl_baski/`: 30 parçanın her biri XY merkezine ve Z=0 seviyesine taşınmıştır.
- `stl_montaj/`: aynı 30 parça, ortak montaj koordinatlarıyla.
- `parcalar.json`: ölçüler, montaj sınırları, baskı ötelemesi. Bölünen parçalarda kesim çizgileri ve pim konumları da vardır.
- `izometrik.png`, `on.png`, `arka.png`, `mesh_kontrol.png`, `parca_katalogu.png`, `bolunmus_parcalar.png`: görünümler.
- `japan_shop_final.blend`: dokulu sahne. Git deposunda yoktur. Yarımların dokusu final6 yüzeyinden aktarıldı, kesim yüzeylerinde düz gri malzeme kullanıldı.

## Geometri kontrolleri

- 30 montaj STL'si ve 30 baskı kopyası: tek bağlı gövde, kapalı yüzey, tutarlı yüz yönü, pozitif hacim; açık/çoklu kenar, dejenere/yinelenen yüz ve kendi içinde kesişme yok (`kontrol_raporu.json`).
- Parçalar arası katı kesişim 0,005 mm³ altında. Pimler deliklere çakışmadan girer (`parcalar_arasi_kontrol.json`).
- Final6'daki 27 bağlantının temas ölçümleri aynen korundu. Buna ek olarak iki kesim yüzeyinin tam oturduğu ölçüldü (`temas_olcumleri.json`).
- Blender sahnesi STL üçgenleriyle birebir eşleşir (`sahne_kontrolu.json`).
