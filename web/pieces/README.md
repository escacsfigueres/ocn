# Piece set

The twelve SVG files in this directory are the **Cburnett** chess pieces
by Colin M.L. Burnett, published on Wikimedia Commons and used by
Wikipedia, Lichess and most of the open chess web.

**Licence: CC BY-SA 3.0.** They are the one part of this repository that
is not MIT (code) or CC-BY-4.0 (catalogue and spec): re-use of the piece
artwork carries the share-alike obligation of its own licence. Nothing
else in OCN depends on them; the board is the only consumer.

They were chosen over drawing our own because they are the set opening
books and encyclopaedias print, and they stay legible at 40 pixels,
which is the size that matters here. `web/build.py` inlines them into
the page as one `<symbol>` sprite at build time.
