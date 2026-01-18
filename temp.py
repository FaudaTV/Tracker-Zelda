from bs4 import BeautifulSoup
import re

# Ton bloc HTML (tronqué pour l'exemple, mais fonctionne sur l'intégralité)
html_data = """
<tbody><tr>
<th style="width:15%">Fuser
</th>
<th style="width:20%">Location
</th>
<th style="width:5%"><span class="term">Kinstone Piece</span>
</th>
<th style="width:5%">Stage
</th>
<th class="unsortable" style="width:50%">Result
</th></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/67/TMC_Ankle_Sprite.png/revision/latest?cb=20200703130342" class="mw-file-description image"><img alt="TMC Ankle Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="24" height="23" class="mw-file-element lazyload" data-image-name="TMC Ankle Sprite.png" data-image-key="TMC_Ankle_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/67/TMC_Ankle_Sprite.png/revision/latest?cb=20200703130342" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Ankle" title="Ankle">Ankle</a>
</td>
<td><a href="/wiki/Lon_Lon_Ranch" title="Lon Lon Ranch">Lon Lon Ranch</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Tree" title="Tree">Tree</a> opens in <a href="/wiki/North_Hyrule_Field" title="North Hyrule Field">North Hyrule Field</a>, leading to a <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a> and a <a href="/wiki/Switch" title="Switch">Switch</a>; when all four <span class="term">Switches</span> are pressed, a <a href="/wiki/Ladder" title="Ladder">Ladder</a> descends, giving <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> access to a <span class="term">Chest</span> containing the <a href="/wiki/Magical_Boomerang" title="Magical Boomerang">Magical Boomerang</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Belari" title="Belari">Belari</a>
</td>
<td><a href="/wiki/Minish_Woods" title="Minish Woods">Minish Woods</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">4
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in the <a href="/wiki/Wind_Ruins" title="Wind Ruins">Wind Ruins</a> containing a <a href="/wiki/Big_Bomb_Bag" class="mw-redirect" title="Big Bomb Bag">Big Bomb Bag</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/6b/TMC_Bremor_Sprite.png/revision/latest?cb=20200703153206" class="mw-file-description image"><img alt="TMC Bremor Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="26" height="29" class="mw-file-element lazyload" data-image-name="TMC Bremor Sprite.png" data-image-key="TMC_Bremor_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/6b/TMC_Bremor_Sprite.png/revision/latest?cb=20200703153206" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Bremor" title="Bremor">Bremor</a>
</td>
<td><a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td><a href="/wiki/Mutoh" title="Mutoh">Mutoh</a> becomes inspired to build a second <a href="/wiki/Vacant_House" title="Vacant House">Vacant House</a> in <a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a> for <a href="/wiki/Gorman" title="Gorman">Gorman</a> to rent.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a9/TMC_Business_Scrub_Sprite.png/revision/latest?cb=20200704145510" class="mw-file-description image"><img alt="TMC Business Scrub Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="67" class="mw-file-element lazyload" data-image-name="TMC Business Scrub Sprite.png" data-image-key="TMC_Business_Scrub_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a9/TMC_Business_Scrub_Sprite.png/revision/latest?cb=20200704145510" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Business_Scrub" title="Business Scrub">Business Scrub</a>
</td>
<td><a href="/wiki/Castor_Wilds" title="Castor Wilds">Castor Wilds</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Tree" title="Tree">Tree</a> opens in <a href="/wiki/Minish_Woods" title="Minish Woods">Minish Woods</a>, containing a <span class="term">Business Scrub</span> that will sell <span class="term">Kinstone Pieces</span>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a9/TMC_Business_Scrub_Sprite.png/revision/latest?cb=20200704145510" class="mw-file-description image"><img alt="TMC Business Scrub Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="67" class="mw-file-element lazyload" data-image-name="TMC Business Scrub Sprite.png" data-image-key="TMC_Business_Scrub_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a9/TMC_Business_Scrub_Sprite.png/revision/latest?cb=20200704145510" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Business_Scrub" title="Business Scrub">Business Scrub</a>
</td>
<td><a href="/wiki/Minish_Woods" title="Minish Woods">Minish Woods</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A crack appears in <a href="/wiki/Castor_Wilds" title="Castor Wilds">Castor Wilds</a> with a <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a> inside.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a9/TMC_Business_Scrub_Sprite.png/revision/latest?cb=20200704145510" class="mw-file-description image"><img alt="TMC Business Scrub Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="67" class="mw-file-element lazyload" data-image-name="TMC Business Scrub Sprite.png" data-image-key="TMC_Business_Scrub_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a9/TMC_Business_Scrub_Sprite.png/revision/latest?cb=20200704145510" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Business_Scrub" title="Business Scrub">Business Scrub</a>
</td>
<td><a href="/wiki/Minish_Woods" title="Minish Woods">Minish Woods</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A <a href="/wiki/Golden_Octorok" title="Golden Octorok">Golden Octorok</a> appears in <a href="/wiki/Western_Wood" title="Western Wood">Western Wood</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/be/TMC_Candy_Sprite.png/revision/latest?cb=20200703160931" class="mw-file-description image"><img alt="TMC Candy Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="20" height="19" class="mw-file-element lazyload" data-image-name="TMC Candy Sprite.png" data-image-key="TMC_Candy_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/be/TMC_Candy_Sprite.png/revision/latest?cb=20200703160931" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Candy_(The_Minish_Cap)" title="Candy (The Minish Cap)">Candy</a>
</td>
<td><a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A shoal rises in <a href="/wiki/Trilby_Highlands" title="Trilby Highlands">Trilby Highlands</a>, allowing <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> to access a <a href="/wiki/Dig_Cavern" title="Dig Cavern">Secret Cave</a> once he has obtained the <a href="/wiki/Flippers" title="Flippers">Flippers</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f8/TMC_Caprice_Sprite.png/revision/latest?cb=20200703122837" class="mw-file-description image"><img alt="TMC Caprice Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="29" class="mw-file-element lazyload" data-image-name="TMC Caprice Sprite.png" data-image-key="TMC_Caprice_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f8/TMC_Caprice_Sprite.png/revision/latest?cb=20200703122837" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Caprice" title="Caprice">Caprice</a>
</td>
<td><a href="/wiki/Home_of_the_Wind_Tribe" title="Home of the Wind Tribe">Home of the Wind Tribe</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in <a href="/wiki/Veil_Falls" title="Veil Falls">Veil Falls</a> containing a blue <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/37/TMC_Damp%C3%A9_Sprite.png/revision/latest?cb=20200703000255" class="mw-file-description image"><img alt="TMC Dampé Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="24" height="22" class="mw-file-element lazyload" data-image-name="TMC Dampé Sprite.png" data-image-key="TMC_Damp%C3%A9_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/37/TMC_Damp%C3%A9_Sprite.png/revision/latest?cb=20200703000255" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Damp%C3%A9" title="Dampé">Dampé</a>
</td>
<td><a href="/wiki/Royal_Valley" title="Royal Valley">Royal Valley</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A crack appears in the <a href="/wiki/Wind_Ruins" title="Wind Ruins">Wind Ruins</a> with a <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a> inside.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/37/TMC_Damp%C3%A9_Sprite.png/revision/latest?cb=20200703000255" class="mw-file-description image"><img alt="TMC Dampé Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="24" height="22" class="mw-file-element lazyload" data-image-name="TMC Dampé Sprite.png" data-image-key="TMC_Damp%C3%A9_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/37/TMC_Damp%C3%A9_Sprite.png/revision/latest?cb=20200703000255" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Damp%C3%A9" title="Dampé">Dampé</a>
</td>
<td><a href="/wiki/Royal_Valley" title="Royal Valley">Royal Valley</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A <a href="/wiki/Tombstone" title="Tombstone">Tombstone</a> opens in the graveyard with <a href="/wiki/Gina" title="Gina">Gina</a> inside, along with a <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> with 100 <a href="/wiki/Mysterious_Shell" class="mw-redirect" title="Mysterious Shell">Mysterious Shells</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e1/TMC_David_Jr._Sprite.png/revision/latest?cb=20200703130242" class="mw-file-description image"><img alt="TMC David Jr. Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="22" height="23" class="mw-file-element lazyload" data-image-name="TMC David Jr. Sprite.png" data-image-key="TMC_David_Jr._Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e1/TMC_David_Jr._Sprite.png/revision/latest?cb=20200703130242" /></a><figcaption></figcaption></figure><br /><a href="/wiki/David_Jr." title="David Jr.">David Jr.</a>
</td>
<td><a href="/wiki/Lake_Hylia" title="Lake Hylia">Lake Hylia</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Tree" title="Tree">Tree</a> opens in <a href="/wiki/North_Hyrule_Field" title="North Hyrule Field">North Hyrule Field</a>, leading to a <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> containing 200 <a href="/wiki/Mysterious_Shell" class="mw-redirect" title="Mysterious Shell">Mysterious Shells</a> and a <a href="/wiki/Switch" title="Switch">Switch</a>; when all four <span class="term">Switches</span> are pressed, a <a href="/wiki/Ladder" title="Ladder">Ladder</a> descends, giving <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> access to a <span class="term">Chest</span> containing the <a href="/wiki/Magical_Boomerang" title="Magical Boomerang">Magical Boomerang</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e1/TMC_David_Jr._Sprite.png/revision/latest?cb=20200703130242" class="mw-file-description image"><img alt="TMC David Jr. Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="22" height="23" class="mw-file-element lazyload" data-image-name="TMC David Jr. Sprite.png" data-image-key="TMC_David_Jr._Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e1/TMC_David_Jr._Sprite.png/revision/latest?cb=20200703130242" /></a><figcaption></figcaption></figure><br /><a href="/wiki/David_Jr." title="David Jr.">David Jr.</a>
</td>
<td><a href="/wiki/Lake_Hylia" title="Lake Hylia">Lake Hylia</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in the <a href="/wiki/Minish" title="Minish">Minish</a>-sized path to <a href="/wiki/Melari%27s_Mine" title="Melari&#39;s Mine">Melari's Mine</a> containing 200 <a href="/wiki/Mysterious_Shell" class="mw-redirect" title="Mysterious Shell">Mysterious Shells</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b5/TMC_Din_Sprite.png/revision/latest?cb=20200703161026" class="mw-file-description image"><img alt="TMC Din Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="20" height="32" class="mw-file-element lazyload" data-image-name="TMC Din Sprite.png" data-image-key="TMC_Din_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b5/TMC_Din_Sprite.png/revision/latest?cb=20200703161026" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Din_(Oracle)" title="Din (Oracle)">Din</a>
</td>
<td><a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A <a href="/wiki/Joy_Butterfly" title="Joy Butterfly">Joy Butterfly</a> appears in the <a href="/wiki/Wind_Ruins" title="Wind Ruins">Wind Ruins</a> that, when collected, allows <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> to shoot <a href="/wiki/Arrow" title="Arrow">Arrows</a> more quickly.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/47/TMC_Eenie_Sprite.png/revision/latest?cb=20200703001154" class="mw-file-description image"><img alt="TMC Eenie Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="57" height="49" class="mw-file-element lazyload" data-image-name="TMC Eenie Sprite.png" data-image-key="TMC_Eenie_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/47/TMC_Eenie_Sprite.png/revision/latest?cb=20200703001154" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Eenie" title="Eenie">Eenie</a>
</td>
<td><a href="/wiki/Eastern_Hills" title="Eastern Hills">Eastern Hills</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>The <a href="/wiki/Goron" title="Goron">Goron</a> at <a href="/wiki/Lon_Lon_Ranch" title="Lon Lon Ranch">Lon Lon Ranch</a> opens the <a href="/wiki/Goron_Cave" title="Goron Cave">Goron Cave</a> (if a <a href="/wiki/Mysterious_Wall" title="Mysterious Wall">Mysterious Wall</a> has already been <span class="term">Fused</span> with, then another <span class="term">Goron</span> will arrive in the <span class="term">Goron Cave</span>).
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4c/TMC_Farore_Sprite.png/revision/latest?cb=20200703161102" class="mw-file-description image"><img alt="TMC Farore Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="21" height="27" class="mw-file-element lazyload" data-image-name="TMC Farore Sprite.png" data-image-key="TMC_Farore_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4c/TMC_Farore_Sprite.png/revision/latest?cb=20200703161102" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Farore_(Oracle)" title="Farore (Oracle)">Farore</a>
</td>
<td><a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td><a href="/wiki/Gorman" title="Gorman">Gorman</a> arrives in <a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>, searching for a young woman to rent out his <a href="/wiki/Vacant_House" title="Vacant House">Vacant House</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4c/TMC_Farore_Sprite.png/revision/latest?cb=20200703161102" class="mw-file-description image"><img alt="TMC Farore Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="21" height="27" class="mw-file-element lazyload" data-image-name="TMC Farore Sprite.png" data-image-key="TMC_Farore_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4c/TMC_Farore_Sprite.png/revision/latest?cb=20200703161102" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Farore_(Oracle)" title="Farore (Oracle)">Farore</a>
</td>
<td><a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A <a href="/wiki/Joy_Butterfly" title="Joy Butterfly">Joy Butterfly</a> appears in <a href="/wiki/Castor_Wilds" title="Castor Wilds">Castor Wilds</a> that, when collected, allows <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> to dig more quickly with the <a href="/wiki/Mole_Mitts" title="Mole Mitts">Mole Mitts</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Fifi_Sprite.png/revision/latest?cb=20200703130311" class="mw-file-description image"><img alt="TMC Fifi Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="22" height="18" class="mw-file-element lazyload" data-image-name="TMC Fifi Sprite.png" data-image-key="TMC_Fifi_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Fifi_Sprite.png/revision/latest?cb=20200703130311" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Fifi" title="Fifi">Fifi</a>
</td>
<td><a href="/wiki/Stockwell%27s_House" title="Stockwell&#39;s House">Stockwell's House</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in the <a href="/wiki/Minish" title="Minish">Minish</a>-sized path to <a href="/wiki/Mayor_Hagen%27s_Lakeside_Cabin" title="Mayor Hagen&#39;s Lakeside Cabin">Mayor Hagen's Lakeside Cabin</a> containing a blue <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e7/TMC_Flurris_Sprite.png/revision/latest?cb=20200703122839" class="mw-file-description image"><img alt="TMC Flurris Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="18" height="29" class="mw-file-element lazyload" data-image-name="TMC Flurris Sprite.png" data-image-key="TMC_Flurris_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e7/TMC_Flurris_Sprite.png/revision/latest?cb=20200703122839" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Flurris" title="Flurris">Flurris</a>
</td>
<td><a href="/wiki/Home_of_the_Wind_Tribe" title="Home of the Wind Tribe">Home of the Wind Tribe</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A <a href="/wiki/Golden_Rope" title="Golden Rope">Golden Rope</a> appears in <a href="/wiki/Castor_Wilds" title="Castor Wilds">Castor Wilds</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e7/TMC_Flurris_Sprite.png/revision/latest?cb=20200703122839" class="mw-file-description image"><img alt="TMC Flurris Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="18" height="29" class="mw-file-element lazyload" data-image-name="TMC Flurris Sprite.png" data-image-key="TMC_Flurris_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e7/TMC_Flurris_Sprite.png/revision/latest?cb=20200703122839" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Flurris" title="Flurris">Flurris</a>
</td>
<td><a href="/wiki/Home_of_the_Wind_Tribe" title="Home of the Wind Tribe">Home of the Wind Tribe</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A fallen <a href="/wiki/Tree" title="Tree">Tree</a> rises in <a href="/wiki/Western_Wood" title="Western Wood">Western Wood</a>, giving access to a patch of dirt where <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> can dig up 300 <a href="/wiki/Rupee" title="Rupee">Rupees</a> with the <a href="/wiki/Mole_Mitts" title="Mole Mitts">Mole Mitts</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a>
</td>
<td><a href="/wiki/Eastern_Hills" title="Eastern Hills">Eastern Hills</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A <a href="/wiki/Bean" title="Bean">Bean</a> grows into a <a href="/wiki/Beanstalk" title="Beanstalk">Beanstalk</a> with a <a href="/wiki/Piece_of_Heart" title="Piece of Heart">Piece of Heart</a> and two <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chests</a> containing 200 <a href="/wiki/Rupee" title="Rupee">Rupees</a> and 200 <a href="/wiki/Mysterious_Shell" class="mw-redirect" title="Mysterious Shell">Mysterious Shells</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a>
</td>
<td><a href="/wiki/Hyrule_Castle_Garden" title="Hyrule Castle Garden">Hyrule Castle Garden</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A fallen <a href="/wiki/Tree" title="Tree">Tree</a> rises in <a href="/wiki/Western_Wood" title="Western Wood">Western Wood</a>, giving access to a patch of dirt where <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> can dig up 400 <a href="/wiki/Rupee" title="Rupee">Rupees</a> with the <a href="/wiki/Mole_Mitts" title="Mole Mitts">Mole Mitts</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a>
</td>
<td><a href="/wiki/Lake_Hylia" title="Lake Hylia">Lake Hylia</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A <a href="/wiki/Bean" title="Bean">Bean</a> grows into a <a href="/wiki/Beanstalk" title="Beanstalk">Beanstalk</a> with a <a href="/wiki/Piece_of_Heart" title="Piece of Heart">Piece of Heart</a> and two <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chests</a> containing 200 <a href="/wiki/Rupee" title="Rupee">Rupees</a> and 200 <a href="/wiki/Mysterious_Shell" class="mw-redirect" title="Mysterious Shell">Mysterious Shells</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a>
</td>
<td><a href="/wiki/Lake_Hylia" title="Lake Hylia">Lake Hylia</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A <a href="/wiki/Tree" title="Tree">Tree</a> opens in <a href="/wiki/Western_Wood" title="Western Wood">Western Wood</a>, containing a <a href="/wiki/Piece_of_Heart" title="Piece of Heart">Piece of Heart</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><span class="mw-default-size" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/55/TMC_Zill_Sprite.png/revision/latest?cb=20200703205758" class="mw-file-description image"><img alt="TMC Zill Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="18" height="22" class="mw-file-element lazyload" data-image-name="TMC Zill Sprite.png" data-image-key="TMC_Zill_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/55/TMC_Zill_Sprite.png/revision/latest?cb=20200703205758" /></a></span><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a> (or <a href="/wiki/Zill" title="Zill">Zill</a>)
</td>
<td><a href="/wiki/Minish_Village" title="Minish Village">Minish Village</a> (or <a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>)
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A <a href="/wiki/Lily_Pad" title="Lily Pad">Lily</a> appears in <a href="/wiki/Castor_Wilds" title="Castor Wilds">Castor Wilds</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><span class="mw-default-size" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/55/TMC_Zill_Sprite.png/revision/latest?cb=20200703205758" class="mw-file-description image"><img alt="TMC Zill Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="18" height="22" class="mw-file-element lazyload" data-image-name="TMC Zill Sprite.png" data-image-key="TMC_Zill_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/55/TMC_Zill_Sprite.png/revision/latest?cb=20200703205758" /></a></span><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a> (or <a href="/wiki/Zill" title="Zill">Zill</a>)
</td>
<td><a href="/wiki/Minish_Village" title="Minish Village">Minish Village</a> (or <a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>)
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A <a href="/wiki/Lily_Pad" title="Lily Pad">Lily</a> appears in <a href="/wiki/Castor_Wilds" title="Castor Wilds">Castor Wilds</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><span class="mw-default-size" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/55/TMC_Zill_Sprite.png/revision/latest?cb=20200703205758" class="mw-file-description image"><img alt="TMC Zill Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="18" height="22" class="mw-file-element lazyload" data-image-name="TMC Zill Sprite.png" data-image-key="TMC_Zill_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/55/TMC_Zill_Sprite.png/revision/latest?cb=20200703205758" /></a></span><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a> (or <a href="/wiki/Zill" title="Zill">Zill</a>)
</td>
<td><a href="/wiki/Minish_Village" title="Minish Village">Minish Village</a> (or <a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>)
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A <a href="/wiki/Lily_Pad" title="Lily Pad">Lily</a> appears in <a href="/wiki/Castor_Wilds" title="Castor Wilds">Castor Wilds</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a>
</td>
<td><a href="/wiki/Minish_Village" title="Minish Village">Minish Village</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">6
</td>
<td>A shoal rises in <a href="/wiki/Veil_Falls" title="Veil Falls">Veil Falls</a>, allowing <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> to access a <a href="/wiki/Dig_Cavern" title="Dig Cavern">Secret Cave</a> with a <a href="/wiki/Piece_of_Heart" title="Piece of Heart">Piece of Heart</a> inside.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a>
</td>
<td><a href="/wiki/Minish_Village" title="Minish Village">Minish Village</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">6
</td>
<td>A crack appears near the <a href="/wiki/Wind_Crest" title="Wind Crest">Wind Crest</a> at <a href="/wiki/Lake_Hylia" title="Lake Hylia">Lake Hylia</a> that leads to <a href="/wiki/Librari" title="Librari">Librari</a>'s home, where he will give <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> a full <a href="/wiki/Heart_Container" title="Heart Container">Heart Container</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a>
</td>
<td><a href="/wiki/Mount_Crenel%27s_Base" title="Mount Crenel&#39;s Base">Mount Crenel's Base</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears at <span class="term">Mount Crenel's Base</span> containing 200 <a href="/wiki/Rupee" title="Rupee">Rupees</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a>
</td>
<td><a href="/wiki/North_Hyrule_Field" title="North Hyrule Field">North Hyrule Field</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in the <a href="/wiki/Wind_Ruins" title="Wind Ruins">Wind Ruins</a> containing 200 <a href="/wiki/Mysterious_Shell" class="mw-redirect" title="Mysterious Shell">Mysterious Shells</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a>
</td>
<td><a href="/wiki/South_Hyrule_Field" title="South Hyrule Field">South Hyrule Field</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="20" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td><a href="/wiki/Syrup" title="Syrup">Syrup</a> is inspired to make the <a href="/wiki/Red_Potion" title="Red Potion">Red Potion</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a>
</td>
<td><a href="/wiki/Trilby_Highlands" title="Trilby Highlands">Trilby Highlands</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A pool in <span class="term">Trilby Highlands</span> is drained, revealing a cave with 75 <a href="/wiki/Rupee" title="Rupee">Rupees</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a>
</td>
<td><a href="/wiki/Western_Wood" title="Western Wood">Western Wood</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A <a href="/wiki/Bean" title="Bean">Bean</a> grows into a <a href="/wiki/Beanstalk" title="Beanstalk">Beanstalk</a> with 320 <a href="/wiki/Rupee" title="Rupee">Rupees</a> and a <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" class="mw-file-description image"><img alt="TMC Forest Picori Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="21" class="mw-file-element lazyload" data-image-name="TMC Forest Picori Sprite.png" data-image-key="TMC_Forest_Picori_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/TMC_Forest_Picori_Sprite.png/revision/latest?cb=20200703104411" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Forest_Picori" title="Forest Picori">Forest Picori</a>
</td>
<td><a href="/wiki/Wind_Ruins" title="Wind Ruins">Wind Ruins</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A <a href="/wiki/Bean" title="Bean">Bean</a> grows into a <a href="/wiki/Beanstalk" title="Beanstalk">Beanstalk</a> with a <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> at the top containing a <a href="/wiki/Large_Quiver" title="Large Quiver">Large Quiver</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/05/TMC_Gale_Sprite.png/revision/latest?cb=20190827003339" class="mw-file-description image"><img alt="TMC Gale Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="28" class="mw-file-element lazyload" data-image-name="TMC Gale Sprite.png" data-image-key="TMC_Gale_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/05/TMC_Gale_Sprite.png/revision/latest?cb=20190827003339" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Gale" title="Gale">Gale</a>
</td>
<td><a href="/wiki/Cloud_Tops" title="Cloud Tops">Cloud Tops</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="20" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A waterfall opens at <a href="/wiki/Veil_Falls" title="Veil Falls">Veil Falls</a> with a <a href="/wiki/Piece_of_Heart" title="Piece of Heart">Piece of Heart</a> inside.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/7b/TMC_Gentari_Sprite.png/revision/latest?cb=20200703130601" class="mw-file-description image"><img alt="TMC Gentari Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="20" height="31" class="mw-file-element lazyload" data-image-name="TMC Gentari Sprite.png" data-image-key="TMC_Gentari_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/7b/TMC_Gentari_Sprite.png/revision/latest?cb=20200703130601" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Gentari" title="Gentari">Gentari</a>
</td>
<td><a href="/wiki/Minish_Village" title="Minish Village">Minish Village</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">4
</td>
<td><a href="/wiki/Belari" title="Belari">Belari</a> is inspired to create the <a href="/wiki/Remote_Bomb" title="Remote Bomb">Remote Bombs</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/28/TMC_Gina_Sprite.png/revision/latest?cb=20200703130528" class="mw-file-description image"><img alt="TMC Gina Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="28" height="25" class="mw-file-element lazyload" data-image-name="TMC Gina Sprite.png" data-image-key="TMC_Gina_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/28/TMC_Gina_Sprite.png/revision/latest?cb=20200703130528" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Gina" title="Gina">Gina</a>
</td>
<td><a href="/wiki/Royal_Valley" title="Royal Valley">Royal Valley</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A fallen <a href="/wiki/Tree" title="Tree">Tree</a> rises in <a href="/wiki/Western_Wood" title="Western Wood">Western Wood</a>, giving access to a <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> containing 100 <a href="/wiki/Mysterious_Shell" class="mw-redirect" title="Mysterious Shell">Mysterious Shells</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/28/TMC_Gina_Sprite.png/revision/latest?cb=20200703130528" class="mw-file-description image"><img alt="TMC Gina Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="28" height="25" class="mw-file-element lazyload" data-image-name="TMC Gina Sprite.png" data-image-key="TMC_Gina_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/28/TMC_Gina_Sprite.png/revision/latest?cb=20200703130528" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Gina" title="Gina">Gina</a>
</td>
<td><a href="/wiki/Royal_Valley" title="Royal Valley">Royal Valley</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A waterfall opens in <a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>, leading to a <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> containing 200 <a href="/wiki/Mysterious_Shell" class="mw-redirect" title="Mysterious Shell">Mysterious Shells</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b5/TMC_Goron_Digger_Sprite.png/revision/latest?cb=20200702214330" class="mw-file-description image"><img alt="TMC Goron Digger Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="28" height="31" class="mw-file-element lazyload" data-image-name="TMC Goron Digger Sprite.png" data-image-key="TMC_Goron_Digger_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b5/TMC_Goron_Digger_Sprite.png/revision/latest?cb=20200702214330" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Goron_Digger" title="Goron Digger">Goron Digger</a>
</td>
<td><a href="/wiki/Lon_Lon_Ranch" title="Lon Lon Ranch">Lon Lon Ranch</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>The <a href="/wiki/Goron_Merchant" title="Goron Merchant">Goron Merchant</a> appears in <a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b5/TMC_Goron_Digger_Sprite.png/revision/latest?cb=20200702214330" class="mw-file-description image"><img alt="TMC Goron Digger Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="28" height="31" class="mw-file-element lazyload" data-image-name="TMC Goron Digger Sprite.png" data-image-key="TMC_Goron_Digger_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b5/TMC_Goron_Digger_Sprite.png/revision/latest?cb=20200702214330" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Goron_Digger" title="Goron Digger">Goron Digger</a>
</td>
<td><a href="/wiki/Goron_Cave" title="Goron Cave">Goron Cave</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">6
</td>
<td><a href="/wiki/Biggoron" title="Biggoron">Biggoron</a> awakens at <a href="/wiki/Veil_Springs" title="Veil Springs">Veil Springs</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/64/TMC_Grayblade_Sprite.png/revision/latest?cb=20200703120216" class="mw-file-description image"><img alt="TMC Grayblade Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="19" height="25" class="mw-file-element lazyload" data-image-name="TMC Grayblade Sprite.png" data-image-key="TMC_Grayblade_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/64/TMC_Grayblade_Sprite.png/revision/latest?cb=20200703120216" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Grayblade" title="Grayblade">Grayblade</a>
</td>
<td><a href="/wiki/Mount_Crenel" title="Mount Crenel">Mount Crenel</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A waterfall opens in <a href="/wiki/Castor_Wilds" title="Castor Wilds">Castor Wilds</a>, leading to <a href="/wiki/Scarblade" title="Scarblade">Scarblade</a>'s dojo.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3e/TMC_Grimblade_Sprite.png/revision/latest?cb=20120125172453" class="mw-file-description image"><img alt="TMC Grimblade Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="24" class="mw-file-element lazyload" data-image-name="TMC Grimblade Sprite.png" data-image-key="TMC_Grimblade_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3e/TMC_Grimblade_Sprite.png/revision/latest?cb=20120125172453" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Grimblade" title="Grimblade">Grimblade</a>
</td>
<td><a href="/wiki/Hyrule_Castle_Garden" title="Hyrule Castle Garden">Hyrule Castle Garden</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A waterfall opens at <a href="/wiki/Veil_Falls" title="Veil Falls">Veil Falls</a>, leading to <a href="/wiki/Splitblade" title="Splitblade">Splitblade</a>'s dojo.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/c6/TMC_Hurdy-Gurdy_Man_Sprite.png/revision/latest?cb=20210927220017" class="mw-file-description image"><img alt="TMC Hurdy-Gurdy Man Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="23" height="35" class="mw-file-element lazyload" data-image-name="TMC Hurdy-Gurdy Man Sprite.png" data-image-key="TMC_Hurdy-Gurdy_Man_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/c6/TMC_Hurdy-Gurdy_Man_Sprite.png/revision/latest?cb=20210927220017" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Hurdy-Gurdy_Man" title="Hurdy-Gurdy Man">Hurdy-Gurdy Man</a>
</td>
<td><a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Tree" title="Tree">Tree</a> opens in <a href="/wiki/South_Hyrule_Field" title="South Hyrule Field">South Hyrule Field</a>, containing a <a href="/wiki/Piece_of_Heart" title="Piece of Heart">Piece of Heart</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/df/TMC_Hailey_Sprite.png/revision/latest?cb=20200703122844" class="mw-file-description image"><img alt="TMC Hailey Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="25" class="mw-file-element lazyload" data-image-name="TMC Hailey Sprite.png" data-image-key="TMC_Hailey_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/df/TMC_Hailey_Sprite.png/revision/latest?cb=20200703122844" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Hailey" title="Hailey">Hailey</a>
</td>
<td><a href="/wiki/Cloud_Tops" title="Cloud Tops">Cloud Tops</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A <a href="/wiki/Golden_Tektite" title="Golden Tektite">Golden Tektite</a> appears at <a href="/wiki/Veil_Falls" title="Veil Falls">Veil Falls</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/ef/TMC_Knuckle_Sprite.png/revision/latest?cb=20200703130726" class="mw-file-description image"><img alt="TMC Knuckle Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="24" height="23" class="mw-file-element lazyload" data-image-name="TMC Knuckle Sprite.png" data-image-key="TMC_Knuckle_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/ef/TMC_Knuckle_Sprite.png/revision/latest?cb=20200703130726" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Knuckle" title="Knuckle">Knuckle</a>
</td>
<td><a href="/wiki/Trilby_Highlands" title="Trilby Highlands">Trilby Highlands</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Tree" title="Tree">Tree</a> opens in <a href="/wiki/North_Hyrule_Field" title="North Hyrule Field">North Hyrule Field</a>, leading to a <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a> and a <a href="/wiki/Switch" title="Switch">Switch</a>; when all four <span class="term">Switches</span> are pressed, a <a href="/wiki/Ladder" title="Ladder">Ladder</a> descends, giving <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> access to a <span class="term">Chest</span> containing the <a href="/wiki/Magical_Boomerang" title="Magical Boomerang">Magical Boomerang</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a5/TMC_Librari_Sprite.png/revision/latest?cb=20200703205101" class="mw-file-description image"><img alt="TMC Librari Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="31" class="mw-file-element lazyload" data-image-name="TMC Librari Sprite.png" data-image-key="TMC_Librari_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a5/TMC_Librari_Sprite.png/revision/latest?cb=20200703205101" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Librari" title="Librari">Librari</a>
</td>
<td><a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A <a href="/wiki/Golden_Octorok" title="Golden Octorok">Golden Octorok</a> appears at the <a href="/wiki/Wind_Ruins" title="Wind Ruins">Wind Ruins</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/1/12/TMC_Mama_Sprite.png/revision/latest?cb=20180928013228" class="mw-file-description image"><img alt="TMC Mama Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="18" height="24" class="mw-file-element lazyload" data-image-name="TMC Mama Sprite.png" data-image-key="TMC_Mama_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/1/12/TMC_Mama_Sprite.png/revision/latest?cb=20180928013228" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mama" title="Mama">Mama</a>
</td>
<td><a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A shoal rises in <a href="/wiki/Lake_Hylia" title="Lake Hylia">Lake Hylia</a>, allowing <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> access to a <a href="/wiki/Dig_Cavern" title="Dig Cavern">Secret Cave</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/fe/TMC_Mayor_Hagen_Sprite.png/revision/latest?cb=20200703205225" class="mw-file-description image"><img alt="TMC Mayor Hagen Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="23" class="mw-file-element lazyload" data-image-name="TMC Mayor Hagen Sprite.png" data-image-key="TMC_Mayor_Hagen_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/fe/TMC_Mayor_Hagen_Sprite.png/revision/latest?cb=20200703205225" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mayor_Hagen" title="Mayor Hagen">Mayor Hagen</a>
</td>
<td><a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A pool drains at <a href="/wiki/Lon_Lon_Ranch" title="Lon Lon Ranch">Lon Lon Ranch</a>, leading to a <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> containing a <a href="/wiki/Big_Wallet" title="Big Wallet">Big Wallet</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/7f/TMC_Meenie_Sprite.png/revision/latest?cb=20200703001202" class="mw-file-description image"><img alt="TMC Meenie Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="57" height="45" class="mw-file-element lazyload" data-image-name="TMC Meenie Sprite.png" data-image-key="TMC_Meenie_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/7f/TMC_Meenie_Sprite.png/revision/latest?cb=20200703001202" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Meenie" title="Meenie">Meenie</a>
</td>
<td><a href="/wiki/Eastern_Hills" title="Eastern Hills">Eastern Hills</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears on the <a href="/wiki/Crenel_Wall" title="Crenel Wall">Crenel Wall</a> containing a blue <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4f/TMC_Melari_Sprite.png/revision/latest?cb=20200703130654" class="mw-file-description image"><img alt="TMC Melari Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="30" height="33" class="mw-file-element lazyload" data-image-name="TMC Melari Sprite.png" data-image-key="TMC_Melari_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4f/TMC_Melari_Sprite.png/revision/latest?cb=20200703130654" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Melari" title="Melari">Melari</a>
</td>
<td><a href="/wiki/Melari%27s_Mine" title="Melari&#39;s Mine">Melari's Mine</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="20" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Bean" title="Bean">Bean</a> grows into a <a href="/wiki/Beanstalk" title="Beanstalk">Beanstalk</a> with a <a href="/wiki/Piece_of_Heart" title="Piece of Heart">Piece of Heart</a> and 160 <a href="/wiki/Rupee" title="Rupee">Rupees</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cf/TMC_Mountain_Minish_Sprite.png/revision/latest?cb=20200703130706" class="mw-file-description image"><img alt="TMC Mountain Minish Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="22" class="mw-file-element lazyload" data-image-name="TMC Mountain Minish Sprite.png" data-image-key="TMC_Mountain_Minish_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cf/TMC_Mountain_Minish_Sprite.png/revision/latest?cb=20200703130706" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mountain_Minish" title="Mountain Minish">Mountain Minish</a>
</td>
<td><a href="/wiki/Melari%27s_Mine" title="Melari&#39;s Mine">Melari's Mine</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in the rainy <a href="/wiki/Minish" title="Minish">Minish</a>-sized path on <a href="/wiki/Mount_Crenel" title="Mount Crenel">Mount Crenel</a> containing a blue <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cf/TMC_Mountain_Minish_Sprite.png/revision/latest?cb=20200703130706" class="mw-file-description image"><img alt="TMC Mountain Minish Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="22" class="mw-file-element lazyload" data-image-name="TMC Mountain Minish Sprite.png" data-image-key="TMC_Mountain_Minish_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cf/TMC_Mountain_Minish_Sprite.png/revision/latest?cb=20200703130706" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mountain_Minish" title="Mountain Minish">Mountain Minish</a>
</td>
<td><a href="/wiki/Melari%27s_Mine" title="Melari&#39;s Mine">Melari's Mine</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in <a href="/wiki/Minish_Woods" title="Minish Woods">Minish Woods</a> containing a blue <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cf/TMC_Mountain_Minish_Sprite.png/revision/latest?cb=20200703130706" class="mw-file-description image"><img alt="TMC Mountain Minish Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="22" class="mw-file-element lazyload" data-image-name="TMC Mountain Minish Sprite.png" data-image-key="TMC_Mountain_Minish_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cf/TMC_Mountain_Minish_Sprite.png/revision/latest?cb=20200703130706" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mountain_Minish" title="Mountain Minish">Mountain Minish</a>
</td>
<td><a href="/wiki/Melari%27s_Mine" title="Melari&#39;s Mine">Melari's Mine</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in the <a href="/wiki/Minish" title="Minish">Minish</a>-sized path on <a href="/wiki/Mount_Crenel" title="Mount Crenel">Mount Crenel</a> near the hot spring containing a blue <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cf/TMC_Mountain_Minish_Sprite.png/revision/latest?cb=20200703130706" class="mw-file-description image"><img alt="TMC Mountain Minish Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="22" class="mw-file-element lazyload" data-image-name="TMC Mountain Minish Sprite.png" data-image-key="TMC_Mountain_Minish_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cf/TMC_Mountain_Minish_Sprite.png/revision/latest?cb=20200703130706" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mountain_Minish" title="Mountain Minish">Mountain Minish</a>
</td>
<td><a href="/wiki/Melari%27s_Mine" title="Melari&#39;s Mine">Melari's Mine</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Golden_Tektite" title="Golden Tektite">Golden Tektite</a> appears on <a href="/wiki/Mount_Crenel" title="Mount Crenel">Mount Crenel</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/02/TMC_Mysterious_Cloud_Sprite.png/revision/latest?cb=20200629200017" class="mw-file-description image"><img alt="TMC Mysterious Cloud Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="41" height="38" class="mw-file-element lazyload" data-image-name="TMC Mysterious Cloud Sprite.png" data-image-key="TMC_Mysterious_Cloud_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/02/TMC_Mysterious_Cloud_Sprite.png/revision/latest?cb=20200629200017" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mysterious_Cloud" title="Mysterious Cloud">Mysterious Cloud</a> (northwest)
</td>
<td><a href="/wiki/Cloud_Tops" title="Cloud Tops">Cloud Tops</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Gold_Sprite_5.png/revision/latest?cb=20190702004756" class="mw-file-description image"><img alt="TMC Kinstone Piece Gold Sprite 5" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="19" height="23" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Gold Sprite 5.png" data-image-key="TMC_Kinstone_Piece_Gold_Sprite_5.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Gold_Sprite_5.png/revision/latest?cb=20190702004756" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A pinwheel begins turning; when all five are turning, a <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Tornado" title="Tornado">Tornado</a></span></span> appears to transport <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> upwards to the <a href="/wiki/Home_of_the_Wind_Tribe" title="Home of the Wind Tribe">Home of the Wind Tribe</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/02/TMC_Mysterious_Cloud_Sprite.png/revision/latest?cb=20200629200017" class="mw-file-description image"><img alt="TMC Mysterious Cloud Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="41" height="38" class="mw-file-element lazyload" data-image-name="TMC Mysterious Cloud Sprite.png" data-image-key="TMC_Mysterious_Cloud_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/02/TMC_Mysterious_Cloud_Sprite.png/revision/latest?cb=20200629200017" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mysterious_Cloud" title="Mysterious Cloud">Mysterious Cloud</a> (center)
</td>
<td><a href="/wiki/Cloud_Tops" title="Cloud Tops">Cloud Tops</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Gold_Sprite_5.png/revision/latest?cb=20190702004756" class="mw-file-description image"><img alt="TMC Kinstone Piece Gold Sprite 5" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="19" height="23" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Gold Sprite 5.png" data-image-key="TMC_Kinstone_Piece_Gold_Sprite_5.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Gold_Sprite_5.png/revision/latest?cb=20190702004756" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A pinwheel begins turning; when all five are turning, a <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Tornado" title="Tornado">Tornado</a></span></span> appears to transport <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> upwards to the <a href="/wiki/Home_of_the_Wind_Tribe" title="Home of the Wind Tribe">Home of the Wind Tribe</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/02/TMC_Mysterious_Cloud_Sprite.png/revision/latest?cb=20200629200017" class="mw-file-description image"><img alt="TMC Mysterious Cloud Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="41" height="38" class="mw-file-element lazyload" data-image-name="TMC Mysterious Cloud Sprite.png" data-image-key="TMC_Mysterious_Cloud_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/02/TMC_Mysterious_Cloud_Sprite.png/revision/latest?cb=20200629200017" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mysterious_Cloud" title="Mysterious Cloud">Mysterious Cloud</a> (southwest)
</td>
<td><a href="/wiki/Cloud_Tops" title="Cloud Tops">Cloud Tops</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/90/TMC_Kinstone_Piece_Gold_Sprite_6.png/revision/latest?cb=20190702004812" class="mw-file-description image"><img alt="TMC Kinstone Piece Gold Sprite 6" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Gold Sprite 6.png" data-image-key="TMC_Kinstone_Piece_Gold_Sprite_6.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/90/TMC_Kinstone_Piece_Gold_Sprite_6.png/revision/latest?cb=20190702004812" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A pinwheel begins turning; when all five are turning, a <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Tornado" title="Tornado">Tornado</a></span></span> appears to transport <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> upwards to the <a href="/wiki/Home_of_the_Wind_Tribe" title="Home of the Wind Tribe">Home of the Wind Tribe</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/02/TMC_Mysterious_Cloud_Sprite.png/revision/latest?cb=20200629200017" class="mw-file-description image"><img alt="TMC Mysterious Cloud Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="41" height="38" class="mw-file-element lazyload" data-image-name="TMC Mysterious Cloud Sprite.png" data-image-key="TMC_Mysterious_Cloud_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/02/TMC_Mysterious_Cloud_Sprite.png/revision/latest?cb=20200629200017" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mysterious_Cloud" title="Mysterious Cloud">Mysterious Cloud</a> (southeast)
</td>
<td><a href="/wiki/Cloud_Tops" title="Cloud Tops">Cloud Tops</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/90/TMC_Kinstone_Piece_Gold_Sprite_6.png/revision/latest?cb=20190702004812" class="mw-file-description image"><img alt="TMC Kinstone Piece Gold Sprite 6" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Gold Sprite 6.png" data-image-key="TMC_Kinstone_Piece_Gold_Sprite_6.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/90/TMC_Kinstone_Piece_Gold_Sprite_6.png/revision/latest?cb=20190702004812" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A pinwheel begins turning; when all five are turning, a <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Tornado" title="Tornado">Tornado</a></span></span> appears to transport <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> upwards to the <a href="/wiki/Home_of_the_Wind_Tribe" title="Home of the Wind Tribe">Home of the Wind Tribe</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/02/TMC_Mysterious_Cloud_Sprite.png/revision/latest?cb=20200629200017" class="mw-file-description image"><img alt="TMC Mysterious Cloud Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="41" height="38" class="mw-file-element lazyload" data-image-name="TMC Mysterious Cloud Sprite.png" data-image-key="TMC_Mysterious_Cloud_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/02/TMC_Mysterious_Cloud_Sprite.png/revision/latest?cb=20200629200017" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mysterious_Cloud" title="Mysterious Cloud">Mysterious Cloud</a> (northeast)
</td>
<td><a href="/wiki/Cloud_Tops" title="Cloud Tops">Cloud Tops</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/dc/TMC_Kinstone_Piece_Gold_Sprite_7.png/revision/latest?cb=20190702004832" class="mw-file-description image"><img alt="TMC Kinstone Piece Gold Sprite 7" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="18" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Gold Sprite 7.png" data-image-key="TMC_Kinstone_Piece_Gold_Sprite_7.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/dc/TMC_Kinstone_Piece_Gold_Sprite_7.png/revision/latest?cb=20190702004832" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A pinwheel begins turning; when all five are turning, a <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Tornado" title="Tornado">Tornado</a></span></span> appears to transport <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> upwards to the <a href="/wiki/Home_of_the_Wind_Tribe" title="Home of the Wind Tribe">Home of the Wind Tribe</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/00/TMC_Mysterious_Statue_Sprite.png/revision/latest?cb=20200831194455" class="mw-file-description image"><img alt="TMC Mysterious Statue Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="32" height="54" class="mw-file-element lazyload" data-image-name="TMC Mysterious Statue Sprite.png" data-image-key="TMC_Mysterious_Statue_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/00/TMC_Mysterious_Statue_Sprite.png/revision/latest?cb=20200831194455" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mysterious_Statue" title="Mysterious Statue">Mysterious Statue</a> (left)
</td>
<td><a href="/wiki/Castor_Wilds" title="Castor Wilds">Castor Wilds</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/fe/TMC_Kinstone_Piece_Gold_Sprite.png/revision/latest?cb=20190702004646" class="mw-file-description image"><img alt="TMC Kinstone Piece Gold Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="18" height="22" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Gold Sprite.png" data-image-key="TMC_Kinstone_Piece_Gold_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/fe/TMC_Kinstone_Piece_Gold_Sprite.png/revision/latest?cb=20190702004646" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A nearby boulder is damaged; when <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> has <strong class="mw-selflink selflink">Fused</strong> with all three <span class="term">Mysterious Statues</span>, the boulder shatters, granting him access to the <a href="/wiki/Wind_Ruins" title="Wind Ruins">Wind Ruins</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/00/TMC_Mysterious_Statue_Sprite.png/revision/latest?cb=20200831194455" class="mw-file-description image"><img alt="TMC Mysterious Statue Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="32" height="54" class="mw-file-element lazyload" data-image-name="TMC Mysterious Statue Sprite.png" data-image-key="TMC_Mysterious_Statue_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/00/TMC_Mysterious_Statue_Sprite.png/revision/latest?cb=20200831194455" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mysterious_Statue" title="Mysterious Statue">Mysterious Statue</a> (center)
</td>
<td><a href="/wiki/Castor_Wilds" title="Castor Wilds">Castor Wilds</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/73/TMC_Kinstone_Piece_Gold_Sprite_2.png/revision/latest?cb=20190702004702" class="mw-file-description image"><img alt="TMC Kinstone Piece Gold Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="20" height="23" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Gold Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Gold_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/73/TMC_Kinstone_Piece_Gold_Sprite_2.png/revision/latest?cb=20190702004702" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A nearby boulder is damaged; when <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> has <strong class="mw-selflink selflink">Fused</strong> with all three <span class="term">Mysterious Statues</span>, the boulder shatters, granting him access to the <a href="/wiki/Wind_Ruins" title="Wind Ruins">Wind Ruins</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/00/TMC_Mysterious_Statue_Sprite.png/revision/latest?cb=20200831194455" class="mw-file-description image"><img alt="TMC Mysterious Statue Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="32" height="54" class="mw-file-element lazyload" data-image-name="TMC Mysterious Statue Sprite.png" data-image-key="TMC_Mysterious_Statue_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/00/TMC_Mysterious_Statue_Sprite.png/revision/latest?cb=20200831194455" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mysterious_Statue" title="Mysterious Statue">Mysterious Statue</a> (right)
</td>
<td><a href="/wiki/Castor_Wilds" title="Castor Wilds">Castor Wilds</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/24/TMC_Kinstone_Piece_Gold_Sprite_3.png/revision/latest?cb=20190702004722" class="mw-file-description image"><img alt="TMC Kinstone Piece Gold Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="18" height="23" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Gold Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Gold_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/24/TMC_Kinstone_Piece_Gold_Sprite_3.png/revision/latest?cb=20190702004722" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A nearby boulder is damaged; when <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> has <strong class="mw-selflink selflink">Fused</strong> with all three <span class="term">Mysterious Statues</span>, the boulder shatters, granting him access to the <a href="/wiki/Wind_Ruins" title="Wind Ruins">Wind Ruins</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/23/TMC_Mysterious_Wall_Sprite.png/revision/latest?cb=20200701204631" class="mw-file-description image"><img alt="TMC Mysterious Wall Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="22" height="22" class="mw-file-element lazyload" data-image-name="TMC Mysterious Wall Sprite.png" data-image-key="TMC_Mysterious_Wall_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/23/TMC_Mysterious_Wall_Sprite.png/revision/latest?cb=20200701204631" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mysterious_Wall" title="Mysterious Wall">Mysterious Wall</a>
</td>
<td><a href="/wiki/Eastern_Hills" title="Eastern Hills">Eastern Hills</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>The <a href="/wiki/Goron" title="Goron">Goron</a> at <a href="/wiki/Lon_Lon_Ranch" title="Lon Lon Ranch">Lon Lon Ranch</a> opens the <a href="/wiki/Goron_Cave" title="Goron Cave">Goron Cave</a> (if <a href="/wiki/Eenie" title="Eenie">Eenie</a> or another <span class="term">Mysterious Wall</span> have already been <span class="term">Fused</span> with, then another <span class="term">Goron</span> will arrive in the <span class="term">Goron Cave</span>).
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/23/TMC_Mysterious_Wall_Sprite.png/revision/latest?cb=20200701204631" class="mw-file-description image"><img alt="TMC Mysterious Wall Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="22" height="22" class="mw-file-element lazyload" data-image-name="TMC Mysterious Wall Sprite.png" data-image-key="TMC_Mysterious_Wall_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/23/TMC_Mysterious_Wall_Sprite.png/revision/latest?cb=20200701204631" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mysterious_Wall" title="Mysterious Wall">Mysterious Wall</a>
</td>
<td><a href="/wiki/Minish_Woods" title="Minish Woods">Minish Woods</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>The <a href="/wiki/Goron" title="Goron">Goron</a> at <a href="/wiki/Lon_Lon_Ranch" title="Lon Lon Ranch">Lon Lon Ranch</a> opens the <a href="/wiki/Goron_Cave" title="Goron Cave">Goron Cave</a> (if <a href="/wiki/Eenie" title="Eenie">Eenie</a> or another <span class="term">Mysterious Wall</span> have already been <span class="term">Fused</span> with, then another <span class="term">Goron</span> will arrive in the <span class="term">Goron Cave</span>).
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/23/TMC_Mysterious_Wall_Sprite.png/revision/latest?cb=20200701204631" class="mw-file-description image"><img alt="TMC Mysterious Wall Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="22" height="22" class="mw-file-element lazyload" data-image-name="TMC Mysterious Wall Sprite.png" data-image-key="TMC_Mysterious_Wall_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/23/TMC_Mysterious_Wall_Sprite.png/revision/latest?cb=20200701204631" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mysterious_Wall" title="Mysterious Wall">Mysterious Wall</a>
</td>
<td><a href="/wiki/Lake_Hylia" title="Lake Hylia">Lake Hylia</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>The <a href="/wiki/Goron" title="Goron">Goron</a> at <a href="/wiki/Lon_Lon_Ranch" title="Lon Lon Ranch">Lon Lon Ranch</a> opens the <a href="/wiki/Goron_Cave" title="Goron Cave">Goron Cave</a> (if <a href="/wiki/Eenie" title="Eenie">Eenie</a> or another <span class="term">Mysterious Wall</span> have already been <span class="term">Fused</span> with, then another <span class="term">Goron</span> will arrive in the <span class="term">Goron Cave</span>).
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/23/TMC_Mysterious_Wall_Sprite.png/revision/latest?cb=20200701204631" class="mw-file-description image"><img alt="TMC Mysterious Wall Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="22" height="22" class="mw-file-element lazyload" data-image-name="TMC Mysterious Wall Sprite.png" data-image-key="TMC_Mysterious_Wall_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/23/TMC_Mysterious_Wall_Sprite.png/revision/latest?cb=20200701204631" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mysterious_Wall" title="Mysterious Wall">Mysterious Wall</a>
</td>
<td><a href="/wiki/Mount_Crenel" title="Mount Crenel">Mount Crenel</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>The <a href="/wiki/Goron" title="Goron">Goron</a> at <a href="/wiki/Lon_Lon_Ranch" title="Lon Lon Ranch">Lon Lon Ranch</a> opens the <a href="/wiki/Goron_Cave" title="Goron Cave">Goron Cave</a> (if <a href="/wiki/Eenie" title="Eenie">Eenie</a> or another <span class="term">Mysterious Wall</span> have already been <span class="term">Fused</span> with, then another <span class="term">Goron</span> will arrive in the <span class="term">Goron Cave</span>).
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/23/TMC_Mysterious_Wall_Sprite.png/revision/latest?cb=20200701204631" class="mw-file-description image"><img alt="TMC Mysterious Wall Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="22" height="22" class="mw-file-element lazyload" data-image-name="TMC Mysterious Wall Sprite.png" data-image-key="TMC_Mysterious_Wall_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/23/TMC_Mysterious_Wall_Sprite.png/revision/latest?cb=20200701204631" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Mysterious_Wall" title="Mysterious Wall">Mysterious Wall</a>
</td>
<td><a href="/wiki/Trilby_Highlands" title="Trilby Highlands">Trilby Highlands</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>The <a href="/wiki/Goron" title="Goron">Goron</a> at <a href="/wiki/Lon_Lon_Ranch" title="Lon Lon Ranch">Lon Lon Ranch</a> opens the <a href="/wiki/Goron_Cave" title="Goron Cave">Goron Cave</a> (if <a href="/wiki/Eenie" title="Eenie">Eenie</a> or another <span class="term">Mysterious Wall</span> have already been <span class="term">Fused</span> with, then another <span class="term">Goron</span> will arrive in the <span class="term">Goron Cave</span>).
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/32/TMC_Nayru_Sprite.png/revision/latest?cb=20200703205321" class="mw-file-description image"><img alt="TMC Nayru Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="21" height="31" class="mw-file-element lazyload" data-image-name="TMC Nayru Sprite.png" data-image-key="TMC_Nayru_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/32/TMC_Nayru_Sprite.png/revision/latest?cb=20200703205321" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Nayru_(Oracle)" title="Nayru (Oracle)">Nayru</a>
</td>
<td><a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="20" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A <a href="/wiki/Joy_Butterfly" title="Joy Butterfly">Joy Butterfly</a> appears in the <a href="/wiki/Royal_Valley" title="Royal Valley">Royal Valley</a> that, when collected, allows <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> to swim more quickly with the <a href="/wiki/Flippers" title="Flippers">Flippers</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/db/TMC_Percy_Sprite.png/revision/latest?cb=20200703000502" class="mw-file-description image"><img alt="TMC Percy Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="29" height="28" class="mw-file-element lazyload" data-image-name="TMC Percy Sprite.png" data-image-key="TMC_Percy_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/db/TMC_Percy_Sprite.png/revision/latest?cb=20200703000502" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Percy" title="Percy">Percy</a>
</td>
<td><a href="/wiki/Trilby_Highlands" title="Trilby Highlands">Trilby Highlands</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="17" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3f/TMC_Kinstone_Piece_Red_Sprite_3.png/revision/latest?cb=20190702005156" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A fallen tree rises in <a href="/wiki/Western_Wood" title="Western Wood">Western Wood</a>, giving <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> access to <a href="/wiki/Percy%27s_House" title="Percy&#39;s House">Percy's House</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a2/TMC_Postman_Sprite.png/revision/latest?cb=20200703205407" class="mw-file-description image"><img alt="TMC Postman Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="27" class="mw-file-element lazyload" data-image-name="TMC Postman Sprite.png" data-image-key="TMC_Postman_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a2/TMC_Postman_Sprite.png/revision/latest?cb=20200703205407" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Postman" title="Postman">Postman</a>
</td>
<td><a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td><a href="/wiki/Marcy" title="Marcy">Marcy</a> appears in the <a href="/wiki/Post_Office" title="Post Office">Post Office</a> and begins selling the <a href="/wiki/Swordsman_Newsletter" title="Swordsman Newsletter"><i>Swordsman Newsletter</i></a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/95/TMC_Siroc_Sprite.png/revision/latest?cb=20200703122845" class="mw-file-description image"><img alt="TMC Siroc Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="26" height="29" class="mw-file-element lazyload" data-image-name="TMC Siroc Sprite.png" data-image-key="TMC_Siroc_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/95/TMC_Siroc_Sprite.png/revision/latest?cb=20200703122845" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Siroc" title="Siroc">Siroc</a>
</td>
<td><a href="/wiki/Home_of_the_Wind_Tribe" title="Home of the Wind Tribe">Home of the Wind Tribe</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in the <a href="/wiki/Royal_Valley" title="Royal Valley">Royal Valley</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/95/TMC_Siroc_Sprite.png/revision/latest?cb=20200703122845" class="mw-file-description image"><img alt="TMC Siroc Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="26" height="29" class="mw-file-element lazyload" data-image-name="TMC Siroc Sprite.png" data-image-key="TMC_Siroc_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/95/TMC_Siroc_Sprite.png/revision/latest?cb=20200703122845" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Siroc" title="Siroc">Siroc</a>
</td>
<td><a href="/wiki/Home_of_the_Wind_Tribe" title="Home of the Wind Tribe">Home of the Wind Tribe</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in the <a href="/wiki/Royal_Valley" title="Royal Valley">Royal Valley</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/bd/TMC_Smith_Sprite.png/revision/latest?cb=20200702213955" class="mw-file-description image"><img alt="TMC Smith Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="20" height="26" class="mw-file-element lazyload" data-image-name="TMC Smith Sprite.png" data-image-key="TMC_Smith_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/bd/TMC_Smith_Sprite.png/revision/latest?cb=20200702213955" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Smith" title="Smith">Smith</a>
</td>
<td><a href="/wiki/South_Hyrule_Field" title="South Hyrule Field">South Hyrule Field</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="20" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in the <a href="/wiki/Eastern_Hills" title="Eastern Hills">Eastern Hills</a> containing an <a href="/wiki/Empty_Bottle" title="Empty Bottle">Empty Bottle</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/bd/TMC_Smith_Sprite.png/revision/latest?cb=20200702213955" class="mw-file-description image"><img alt="TMC Smith Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="20" height="26" class="mw-file-element lazyload" data-image-name="TMC Smith Sprite.png" data-image-key="TMC_Smith_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/bd/TMC_Smith_Sprite.png/revision/latest?cb=20200702213955" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Smith" title="Smith">Smith</a>
</td>
<td><a href="/wiki/South_Hyrule_Field" title="South Hyrule Field">South Hyrule Field</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in <a href="/wiki/Trilby_Highlands" title="Trilby Highlands">Trilby Highlands</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/76/TMC_Source_of_the_Flow_Sprite.png/revision/latest?cb=20200701204636" class="mw-file-description image"><img alt="TMC Source of the Flow Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="32" height="27" class="mw-file-element lazyload" data-image-name="TMC Source of the Flow Sprite.png" data-image-key="TMC_Source_of_the_Flow_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/76/TMC_Source_of_the_Flow_Sprite.png/revision/latest?cb=20200701204636" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Source_of_the_Flow" title="Source of the Flow">Source of the Flow</a>
</td>
<td><a href="/wiki/Veil_Falls" title="Veil Falls">Veil Falls</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/64/TMC_Kinstone_Piece_Gold_Sprite_4.png/revision/latest?cb=20190702004738" class="mw-file-description image"><img alt="TMC Kinstone Piece Gold Sprite 4" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="21" height="21" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Gold Sprite 4.png" data-image-key="TMC_Kinstone_Piece_Gold_Sprite_4.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/64/TMC_Kinstone_Piece_Gold_Sprite_4.png/revision/latest?cb=20190702004738" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>The stone slab at the end of the bridge opens, granting <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> access to the caves of <a href="/wiki/Veil_Falls" title="Veil Falls">Veil Falls</a> that lead to <a href="/wiki/Veil_Springs" title="Veil Springs">Veil Springs</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5f/TMC_Spekter_Sprite.png/revision/latest?cb=20200703130551" class="mw-file-description image"><img alt="TMC Spekter Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="20" height="26" class="mw-file-element lazyload" data-image-name="TMC Spekter Sprite.png" data-image-key="TMC_Spekter_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5f/TMC_Spekter_Sprite.png/revision/latest?cb=20200703130551" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Spekter" title="Spekter">Spekter</a>
</td>
<td><a href="/wiki/Royal_Valley" title="Royal Valley">Royal Valley</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">4
</td>
<td><a href="/wiki/Borlov" title="Borlov">Borlov</a> creates a harder difficulty in the <a href="/wiki/Chest_Mini-Game_Shop" title="Chest Mini-Game Shop">Chest Mini-Game Shop</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5f/TMC_Spekter_Sprite.png/revision/latest?cb=20200703130551" class="mw-file-description image"><img alt="TMC Spekter Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="20" height="26" class="mw-file-element lazyload" data-image-name="TMC Spekter Sprite.png" data-image-key="TMC_Spekter_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5f/TMC_Spekter_Sprite.png/revision/latest?cb=20200703130551" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Spekter" title="Spekter">Spekter</a>
</td>
<td><a href="/wiki/Royal_Valley" title="Royal Valley">Royal Valley</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/TMC_Kinstone_Piece_Blue_Sprite.png/revision/latest?cb=20190702004425" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">4
</td>
<td><a href="/wiki/Spookter" title="Spookter">Spookter</a> leaves <a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>, giving <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> access to the inside of <a href="/wiki/Anju%27s_Henhouse" class="mw-redirect" title="Anju&#39;s Henhouse">Anju's Henhouse</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/6b/TMC_Strato_Sprite.png/revision/latest?cb=20190715201048" class="mw-file-description image"><img alt="TMC Strato Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="16" height="26" class="mw-file-element lazyload" data-image-name="TMC Strato Sprite.png" data-image-key="TMC_Strato_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/6b/TMC_Strato_Sprite.png/revision/latest?cb=20190715201048" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Strato" title="Strato">Strato</a>
</td>
<td><a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Portal_(Object)" title="Portal (Object)">Portal</a> appears in <a href="/wiki/South_Hyrule_Field" title="South Hyrule Field">South Hyrule Field</a> that leads to the <a href="/wiki/Home_of_the_Wind_Tribe" title="Home of the Wind Tribe">Home of the Wind Tribe</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/99/TMC_Tina_Sprite.png/revision/latest?cb=20200703205719" class="mw-file-description image"><img alt="TMC Tina Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="20" height="31" class="mw-file-element lazyload" data-image-name="TMC Tina Sprite.png" data-image-key="TMC_Tina_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/99/TMC_Tina_Sprite.png/revision/latest?cb=20200703205719" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Tina" title="Tina">Tina</a>
</td>
<td><a href="/wiki/Hyrule_Town" class="mw-redirect" title="Hyrule Town">Hyrule Town</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in <a href="/wiki/Trilby_Highlands" title="Trilby Highlands">Trilby Highlands</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d7/TMC_Tingle_Sprite.png/revision/latest?cb=20200703130628" class="mw-file-description image"><img alt="TMC Tingle Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="20" height="25" class="mw-file-element lazyload" data-image-name="TMC Tingle Sprite.png" data-image-key="TMC_Tingle_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d7/TMC_Tingle_Sprite.png/revision/latest?cb=20200703130628" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Tingle" title="Tingle">Tingle</a>
</td>
<td><a href="/wiki/South_Hyrule_Field" title="South Hyrule Field">South Hyrule Field</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">2
</td>
<td>A <a href="/wiki/Tree" title="Tree">Tree</a> opens in <a href="/wiki/North_Hyrule_Field" title="North Hyrule Field">North Hyrule Field</a>, leading to a <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a> and a <a href="/wiki/Switch" title="Switch">Switch</a>; when all four <span class="term">Switches</span> are pressed, a <a href="/wiki/Ladder" title="Ladder">Ladder</a> descends, giving <span class="facelift-term-invalid"><span title="Invalid or missing term" class="explain"><a href="/wiki/Link" title="Link">Link</a></span></span> access to a <span class="term">Chest</span> containing the <a href="/wiki/Magical_Boomerang" title="Magical Boomerang">Magical Boomerang</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d7/TMC_Tingle_Sprite.png/revision/latest?cb=20200703130628" class="mw-file-description image"><img alt="TMC Tingle Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="20" height="25" class="mw-file-element lazyload" data-image-name="TMC Tingle Sprite.png" data-image-key="TMC_Tingle_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d7/TMC_Tingle_Sprite.png/revision/latest?cb=20200703130628" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Tingle" title="Tingle">Tingle</a>
</td>
<td><a href="/wiki/South_Hyrule_Field" title="South Hyrule Field">South Hyrule Field</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/c/cc/TMC_Kinstone_Piece_Red_Sprite.png/revision/latest?cb=20190702005126" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">3
</td>
<td>A <a href="/wiki/Golden_Tektite" title="Golden Tektite">Golden Tektite</a> appears on <a href="/wiki/Mount_Crenel" title="Mount Crenel">Mount Crenel</a>.
</td></tr>
<tr>
<td style="text-align:center"><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/8/8d/TMC_Waveblade_Sprite.png/revision/latest?cb=20200703120045" class="mw-file-description image"><img alt="TMC Waveblade Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="19" height="25" class="mw-file-element lazyload" data-image-name="TMC Waveblade Sprite.png" data-image-key="TMC_Waveblade_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/8/8d/TMC_Waveblade_Sprite.png/revision/latest?cb=20200703120045" /></a><figcaption></figcaption></figure><br /><a href="/wiki/Waveblade" title="Waveblade">Waveblade</a>
</td>
<td><a href="/wiki/Lake_Hylia" title="Lake Hylia">Lake Hylia</a>
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="20" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">5
</td>
<td>A waterfall opens in <a href="/wiki/North_Hyrule_Field" title="North Hyrule Field">North Hyrule Field</a>, leading to <a href="/wiki/Greatblade" title="Greatblade">Greatblade</a>'s dojo.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" class="mw-file-description image"><img alt="TMC Kinstone Piece Blue Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Blue Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Blue_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/20/TMC_Kinstone_Piece_Blue_Sprite_2.png/revision/latest?cb=20190702004410" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Tree" title="Tree">Tree</a> opens in <a href="/wiki/North_Hyrule_Field" title="North Hyrule Field">North Hyrule Field</a>, containing a <a href="/wiki/Fairy_Fountain" title="Fairy Fountain">Fairy Fountain</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A pool in <a href="/wiki/Hyrule_Castle_Garden" title="Hyrule Castle Garden">Hyrule Castle Garden</a> is drained, leading to a <a href="/wiki/Fairy_Fountain" title="Fairy Fountain">Fairy Fountain</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A pool in <a href="/wiki/South_Hyrule_Field" title="South Hyrule Field">South Hyrule Field</a> is drained, leading to a cave with 75 <a href="/wiki/Rupee" title="Rupee">Rupees</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Golden_Octorok" title="Golden Octorok">Golden Octorok</a> appears in <a href="/wiki/Minish_Woods" title="Minish Woods">Minish Woods</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Golden_Rope" title="Golden Rope">Golden Rope</a> appears in the <a href="/wiki/Eastern_Hills" title="Eastern Hills">Eastern Hills</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Golden_Rope" title="Golden Rope">Golden Rope</a> appears in <a href="/wiki/Hyrule_Castle_Garden" title="Hyrule Castle Garden">Hyrule Castle Garden</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A crack appears in <a href="/wiki/Minish_Woods" title="Minish Woods">Minish Woods</a> near the entrance to the <a href="/wiki/Minish_Village" title="Minish Village">Minish Village</a>, leading to a <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> containing a blue <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in the <a href="/wiki/Minish" title="Minish">Minish</a>-sized path at <a href="/wiki/Funday_School" title="Funday School">Funday School</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in the <a href="/wiki/Minish" title="Minish">Minish</a>-sized path at <a href="/wiki/Lon_Lon_Ranch" title="Lon Lon Ranch">Lon Lon Ranch</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in the <a href="/wiki/Minish" title="Minish">Minish</a>-sized path leading to the <a href="/wiki/Minish_Village" title="Minish Village">Minish Village</a> containing 200 <a href="/wiki/Rupee" title="Rupee">Rupees</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in <a href="/wiki/Minish_Woods" title="Minish Woods">Minish Woods</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in <a href="/wiki/Minish_Woods" title="Minish Woods">Minish Woods</a> containing a red <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in <a href="/wiki/Minish_Woods" title="Minish Woods">Minish Woods</a> containing 200 <a href="/wiki/Rupee" title="Rupee">Rupees</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in <a href="/wiki/Minish_Woods" title="Minish Woods">Minish Woods</a> containing a blue <a href="/wiki/Kinstone_Piece" title="Kinstone Piece">Kinstone Piece</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/63/TMC_Kinstone_Piece_Green_Sprite_2.png/revision/latest?cb=20190702005001" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears at <a href="/wiki/Lon_Lon_Ranch" title="Lon Lon Ranch">Lon Lon Ranch</a> containing 200 <a href="/wiki/Rupee" title="Rupee">Rupees</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="14" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/5d/TMC_Kinstone_Piece_Green_Sprite.png/revision/latest?cb=20190702004946" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in <a href="/wiki/North_Hyrule_Field" title="North Hyrule Field">North Hyrule Field</a> containing 200 <a href="/wiki/Mysterious_Shell" class="mw-redirect" title="Mysterious Shell">Mysterious Shells</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" class="mw-file-description image"><img alt="TMC Kinstone Piece Green Sprite 3" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="24" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Green Sprite 3.png" data-image-key="TMC_Kinstone_Piece_Green_Sprite_3.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d8/TMC_Kinstone_Piece_Green_Sprite_3.png/revision/latest?cb=20190702005018" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A <a href="/wiki/Treasure_Chest" title="Treasure Chest">Chest</a> appears in <a href="/wiki/South_Hyrule_Field" title="South Hyrule Field">South Hyrule Field</a> containing 200 <a href="/wiki/Mysterious_Shell" class="mw-redirect" title="Mysterious Shell">Mysterious Shells</a>.
</td></tr>
<tr>
<td style="text-align:center">Random
</td>
<td>N/A
</td>
<td><figure class="mw-default-size mw-halign-center" typeof="mw:File"><a href="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" class="mw-file-description image"><img alt="TMC Kinstone Piece Red Sprite 2" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="15" height="20" class="mw-file-element lazyload" data-image-name="TMC Kinstone Piece Red Sprite 2.png" data-image-key="TMC_Kinstone_Piece_Red_Sprite_2.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/TMC_Kinstone_Piece_Red_Sprite_2.png/revision/latest?cb=20190702005143" /></a><figcaption></figcaption></figure>
</td>
<td style="text-align:center">1
</td>
<td>A fountain in <a href="/wiki/Hyrule_Castle_Garden" title="Hyrule Castle Garden">Hyrule Castle Garden</a> drains, leading to a <a href="/wiki/Piece_of_Heart" title="Piece of Heart">Piece of Heart</a>.
</td></tr></tbody></table>
<h2><span class="mw-headline" id="Nomenclature">Nomenclature</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a title="Sign in to edit" data-tracking-label="log-in-edit-section" data-action="edit-section" href="https://auth.fandom.com/signin?redirect=https%3A%2F%2Fzelda.fandom.com%2Fwiki%2FKinstone_Fusion%3Faction%3Dedit%26section%3D5&amp;uselang=en" data-testid="log-in-edit-section" class="mw-editsection-visualeditor" aria-label="Sign in to edit"><svg class="wds-icon wds-icon-tiny" aria-hidden="true" focusable="false"><use xlink:href="#wds-icons-pencil-tiny"></use></svg></a><span class="mw-editsection-bracket">]</span></span></h2>
<table class="wikitable" style="margin:1em 0; font-size: 95%;">
<tbody><tr>
<th colspan="4" style="font-size:110%;"><span typeof="mw:File"><span><img alt="TMC Forest Minish Artwork" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="20" height="31" class="mw-file-element lazyload" data-image-name="TMC Forest Minish Artwork.png" data-image-key="TMC_Forest_Minish_Artwork.png" data-relevant="1" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/af/TMC_Forest_Minish_Artwork.png/revision/latest/scale-to-width-down/20?cb=20111230062730" /></span></span> Names in Other Regions <span class="mw-default-size" typeof="mw:File"><span><img alt="TMC Jabber Nut Sprite" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" loading="lazy" width="13" height="15" class="mw-file-element lazyload" data-image-name="TMC Jabber Nut Sprite.png" data-image-key="TMC_Jabber_Nut_Sprite.png" data-relevant="0" data-src="https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b3/TMC_Jabber_Nut_Sprite.png/revision/latest?cb=20181006152219" /></span></span>
</th></tr>
<tr>
<th colspan="2">Language
</th>
<th>Name
</th>
<th>Meaning
</th></tr>
"""

def parse_kinstones(html):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('tr')[1:]  # On saute l'en-tête
    
    # Dictionnaires pour stocker les totaux
    results = {
        "Green": {"1": 0, "2": 0, "3": 0},
        "Blue": {"1": 0, "2": 0},
        "Red": {"1": 0, "2": 0, "3": 0},
        "Gold": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0}
    }

    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 3: continue
        
        # Extraction de l'URL de l'image de la pièce
        img_tag = cols[2].find('img')
        if not img_tag: continue
        
        # On récupère le nom du fichier image (ex: TMC_Kinstone_Piece_Green_Sprite_3.png)
        # data-src ou src selon le cas
        img_url = img_tag.get('data-src') or img_tag.get('src')
        
        # Logique de détection par couleur et motif
        color = None
        for c in ["Green", "Blue", "Red", "Gold"]:
            if c in img_url:
                color = c
                break
        
        if color:
            # Chercher le chiffre à la fin du nom de fichier (ex: Sprite_3 -> 3)
            # Si pas de chiffre, c'est le motif par défaut (1)
            match = re.search(r'Sprite_(\d+)', img_url)
            motif = match.group(1) if match else "1"
            
            # Cas particulier pour l'Or qui utilise des IDs spécifiques dans ton tableau
            if color == "Gold":
                match_gold = re.search(r'Gold_Sprite_(\d+)', img_url)
                motif = match_gold.group(1) if match_gold else "1"

            if motif in results[color]:
                results[color][motif] += 1
            else:
                results[color][motif] = 1

    return results

# Exécution et affichage
stats = parse_kinstones(html_data)

print("--- NOMBRE DE PIÈCES PAR TYPE ---")
for color, motifs in stats.items():
    for motif_id, count in motifs.items():
        if count > 0:
            print(f"{color} {motif_id}: {count}")