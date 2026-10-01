import re
import unicodedata

PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
ASCII_DIGITS = "0123456789"

DIGIT_TRANSLATION = str.maketrans(
    PERSIAN_DIGITS + ARABIC_DIGITS,
    ASCII_DIGITS + ASCII_DIGITS,
)

CHAR_TRANSLATION = str.maketrans({
    "ي": "ی",
    "ى": "ی",
    "ك": "ک",
    "ۀ": "ه",
    "ة": "ه",
    "ؤ": "و",
    "إ": "ا",
    "أ": "ا",
})


def normalize_text(value: str | None) -> str:
    if not value:
        return ""

    text = unicodedata.normalize("NFKC", value)
    text = text.translate(DIGIT_TRANSLATION)
    text = text.translate(CHAR_TRANSLATION)
    text = text.replace("\u200c", " ")
    text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
    text = re.sub(r"[^\w\s+#@.-]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def compact_cta(value: str | None) -> str:
    text = normalize_text(value)
    text = re.sub(r"\b(عدد|کلمه|لطفا|لطفاً|من|هم|بفرست|ارسال|کن|کامنت)\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" .-_")
    return text
