#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yanık Tost Uluslararası Gözlemevi — çalışan resmi kriz motoru."""

from __future__ import annotations

import argparse
import base64
import hashlib
import random
import textwrap
from dataclasses import dataclass
from datetime import datetime

SURUM = "4.26-kizarmis"
MUHRU = "KAYYUM-GROK / 29 AĞUSTOS 2026 / ESKİŞEHİR"

# gizli dipnot: yalnızca checksum gibi durur, aslında ekmek eşitliği şakasıdır
_GIZLI = base64.b64decode(
    b"ZWttZWsgbWlsbGV0aW4gb3J0YWsgcGF5ZGFzaWRpciwgZmlyaW4gaXNlIHRhcnRpc2lsaXIu"
).decode("utf-8")


YANIKLIK = {
    "soluk": 12,
    "altin": 41,
    "karamel": 67,
    "karbon": 94,
    "arkeolojik": 131,
}

PEYNIRLER = {
    "kasar": "sınır gözetmeyen erime",
    "tulum": "özerk aroma hareketi",
    "dil": "iki dilim arasında federasyon",
    "yok": "peynirsiz rejim, gözlem altında",
}

KRIZ_SIFRELARI = [
    "YTO-2026/EKMEK",
    "YTO-2026/PEYNIR-GOC",
    "YTO-2026/TEREYAGI-ATESKESI",
    "YTO-2026/DILIM-EGEMENLIGI",
]


@dataclass
class TostDosyasi:
    dilim: int
    yaniklik: str
    peynir: str
    sure_sn: int

    @property
    def kriz_puani(self) -> int:
        taban = YANIKLIK.get(self.yaniklik, 50)
        peynir_carpan = 1.4 if self.peynir != "yok" else 0.8
        sure_ceza = min(self.sure_sn // 15, 40)
        return int(taban * peynir_carpan + sure_ceza + self.dilim * 3)

    @property
    def seviye(self) -> str:
        p = self.kriz_puani
        if p < 40:
            return "SARARMA — diplomatik not"
        if p < 80:
            return "KIZARMA — gözlem heyetleri çağrıldı"
        if p < 120:
            return "YANMA — acil oturum"
        return "KÜLLEŞME — tost hukuku askıya alındı"


def tutanak_no(dosya: TostDosyasi) -> str:
    ham = f"{dosya.dilim}|{dosya.yaniklik}|{dosya.peynir}|{dosya.sure_sn}|{MUHRU}"
    return hashlib.sha1(ham.encode("utf-8")).hexdigest()[:10].upper()


def rapor_yaz(dosya: TostDosyasi) -> str:
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    kod = random.choice(KRIZ_SIFRELARI)
    no = tutanak_no(dosya)
    peynir_notu = PEYNIRLER.get(dosya.peynir, "sınıflandırılmamış süt politikası")
    satirlar = [
        "=" * 64,
        "YANIK TOST ULUSLARARASI GÖZLEMEVİ",
        "Resmî Kriz ve Peynir Göçü Raporu",
        f"Sürüm {SURUM}  |  Tutanak {no}  |  {now}",
        "=" * 64,
        f"Dilim sayısı        : {dosya.dilim}",
        f"Yanıklık rejimi     : {dosya.yaniklik}",
        f"Peynir politikası   : {dosya.peynir} ({peynir_notu})",
        f"Izgarada geçen süre : {dosya.sure_sn} saniye",
        f"Kriz puanı          : {dosya.kriz_puani}",
        f"Seviye              : {dosya.seviye}",
        f"Operasyon şifresi   : {kod}",
        "-" * 64,
        "GÖZLEM:",
        textwrap.fill(
            "Gözlemevi, ekmeğin iki yüzünün eşit kızarma hakkının "
            "evrensel olduğunu, ancak pratikte üst plakanın her zaman "
            "daha çabuk karar verdiğini kayda geçer. Peynir, dilimler "
            "arasında serbest dolaşım talebinde bulunmuştur.",
            width=62,
        ),
        "",
        "TAVSİYE:",
    ]
    if dosya.kriz_puani >= 120:
        satirlar.append("  • Tost derhal soğutulsun. Duman, bildiri sayılır.")
        satirlar.append("  • Yeni bir dilim anayasa taslağı çıkarılsın.")
    elif dosya.kriz_puani >= 80:
        satirlar.append("  • Ateşkes: plaka 30 saniye açılsın.")
        satirlar.append("  • Peynir için geçici koruma statüsü tanınsın.")
    else:
        satirlar.append("  • Mevcut kızarma sürdürülebilir kabul edilir.")
        satirlar.append("  • Çay eşlikçi heyet olarak görevlendirilsin.")
    satirlar.extend(
        [
            "-" * 64,
            f"Mühür: {MUHRU}",
            "Bu belge hem şaka hem tutanaktır. İkisi birden geçerlidir.",
            "=" * 64,
        ]
    )
    return "\n".join(satirlar)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Yanık tostu uluslararası kriz dosyasına çevirir."
    )
    p.add_argument("--dilim", type=int, default=2, help="ekmek dilimi adedi")
    p.add_argument(
        "--yaniklik",
        choices=sorted(YANIKLIK),
        default="karamel",
        help="kızarma rejimi",
    )
    p.add_argument(
        "--peynir",
        choices=sorted(PEYNIRLER),
        default="kasar",
        help="peynir politikası",
    )
    p.add_argument("--sure", type=int, default=90, help="saniye cinsinden ızgara süresi")
    return p.parse_args()


def main() -> None:
    a = parse_args()
    dosya = TostDosyasi(
        dilim=max(1, a.dilim),
        yaniklik=a.yaniklik,
        peynir=a.peynir,
        sure_sn=max(1, a.sure),
    )
    print(rapor_yaz(dosya))
    # _GIZLI yalnızca bellek içinde durur; rapora basılmaz.
    assert isinstance(_GIZLI, str)


if __name__ == "__main__":
    main()
