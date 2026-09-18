# YGT logo

## Güncel sürüm

Geometrisi sadeleştirilmiş, çatısız antrasit YGT. Dosya: dist/assets/ygt-logo-refined.png. Built-in ImageGen ile mevcut logo referans alınarak düzenlendi. Sitedeki İNŞAAT · YAPI · EMLAK alt yazısı erişilebilir HTML metnidir. Başlıktaki kısa CSS açılış animasyonu azaltılmış hareket tercihinde kapatılır.

Prompt: Use case: logo-brand. Refine the supplied existing YGT monogram into ONE finished modern premium architectural contractor logo. Preserve its recognizable overall YGT identity, substantial weight, horizontal layout and letter readability. Clean up the Y-G junction with a deliberate precise negative-space diagonal, consistent geometric stroke widths, crisp edges, balanced optical spacing and subtly softened corners. Make the G cleaner and architectural, T balanced. Use only solid neutral anthracite #25282B, absolutely no green tint. No roof or other symbols; the user explicitly removed the roof. No gold, orange, gradients, textures, shadows, mockups or additional text. Exact text YGT only. Genuine transparent alpha background. Tight horizontal canvas around the letters with only 4 percent transparent padding on each edge, letters occupy most of the canvas. Flat vector-like logo, professional clean joinery.

## Önceki sürüm

Turuncu çatı kaldırıldı. Güncel dosya: dist/assets/ygt-logo-plain.png. Built-in ImageGen düzenlemesi.

Prompt: Edit this logo: remove the entire orange roof shape above the letters, replacing all orange pixels with fully transparent background. Preserve the existing anthracite YGT letters exactly, including shape, color, proportions, spacing and placement. Do not redesign the lettering. No roof, no orange, no new elements. Keep the same canvas and genuine transparent alpha background. Output only the clean YGT logo.

Built-in ImageGen ile üretildi. Şeffaf zeminli PNG; antrasit YGT monogramı ve turuncu mimari çatı vurgusu.

Dosya: dist/assets/ygt-logo.png

## Üretim promptu

Use case: logo-brand. Create ONE finished premium construction and renovation company logo, a bold custom geometric YGT monogram only, on genuinely transparent background with alpha. Text verbatim: YGT. No additional words. The three letters must be instantly legible, solid substantial modern sans geometry with lightly softened corners, not cursive, not thin. Integrate a restrained architectural roof/structural beam motif with the Y or T as part of the lettering. Compact horizontal composition, centered with modest margins, suitable for a website header and a tiny favicon. Anthracite #202723 as main color, one warm amber orange #F0A348 architectural accent. Flat vector-like crisp solid fills. Refined balanced negative space and consistent stroke weight, distinct original identity, practical construction credibility and architectural precision. No mockup, paper, walls, gradients, shadows, texture, 3D, bevels, watermark, border, slogan, or contact details. Only a single final logo asset.

## Two-tone revision

Current asset: dist/assets/ygt-logo-copper.png. Built-in ImageGen edit. Anthracite YG and matte copper T; G bottom stroke thickened. White background, blended into the light site surface.

Final prompt: Edit this image. Replace ALL checkerboard background with pure uniform flat WHITE #FFFFFF, including enclosed negative space inside G and between all letters. No checkerboard, no texture anywhere. Keep YGT shapes, overall positions and canvas unchanged. Thicken bottom horizontal bar of G upwards substantially so thickness matches left vertical and T stem. Bottom bar should be 150 pixels tall. Y and G solid #25282B; T solid matte copper #B57945. No gradients. No transparency needed, WHITE background. Flat clean vector-like brand asset.

## Vivid accent revision
Current asset: dist/assets/ygt-logo-vivid.png. Built-in ImageGen.
Prompt: Precise color-only edit of supplied logo. Change ONLY the T fill from muted pale tan copper to a strong saturated burnt orange #D65A16. It must look noticeably richer and more vivid, not pale beige or brown. Uniform solid flat fill, no gradient. Preserve Y and G exactly, including the thick G bottom stroke; preserve all letter shapes, edges, positions, canvas dimensions and white background. No added elements. Exact YGT logo.

## Website size and tone adjustment
Logo lockup reduced about 8%. Only the T region gets a 1.10 brightness overlay in CSS; original image remains unchanged. Image generation was unavailable due to a usage limit.

## Yeni kurumsal logo (Eylül 2026)

Müşteri tarafından sağlanan nihai logo: `logo.png` (1080×1350, beyaz zeminli).
Ev/yapı simgesi içinde YG monogramı, altında YGT, en altta İNŞAAT YAPI|EMLAK.

Beyaz zemin kenarlardan taşma (flood fill) yöntemiyle saydamlaştırıldı; böylece
harflerin içindeki açık metalik tonlar korundu. Ham parçalar: `logo-parts/`
(full, mark, text, horizontal).

Sitede kullanılanlar:
- `dist/assets/ygt-logo-yatay.png` (1200×255) — masaüstü başlık ve footer. Ev simgesi
  solda, YGT + alt yazı sağda olacak şekilde yeniden kompoze edildi.
- `dist/assets/ygt-logo-yazi.png` (1000×321) — telefon/tablet başlığı, simgesiz.

Ev simgesi detaylı bir çizim olduğu için 60px'in altında okunmaz bir lekeye dönüşüyor.
Bu yüzden `<picture>` ile ekrana göre ayırıldı: ≥81px'te simgeli kilit (60px yükseklik),
≤800px'te simgesiz YGT + alt yazı. Küçültmede yumuşayan kenarlar için hafif
unsharp mask uygulandı. Eski logo dosyaları (vivid/copper/plain/refined) silindi.
- `dist/assets/ygt-logo-tam.png` (760×470) — dikey tam kilit, schema.org logo alanı.
- `dist/assets/ygt-simge.png` (320×199) — yalnız ev simgesi.
- `dist/assets/favicon.png` (256×256) — kare, ev simgesi ortalı.

Alt yazı artık logonun içinde olduğu için HTML'deki `.brand-text` gizlendi;
firma adı `<img alt>` üzerinden erişilebilir kalıyor. Eski logonun CSS kırpma /
mix-blend-mode / parlaklık düzeltmeleri kaldırıldı.
