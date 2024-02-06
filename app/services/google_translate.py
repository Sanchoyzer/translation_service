from typing import ClassVar, Self

import httpx

from app.schemas.google_translate import TranslationSchema


class GoogleTranslateService:
    USER_AGENT: ClassVar[str] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    """Inspired by googletrans lib."""

    NAME_MAPPING: ClassVar[dict[int, str]] = {
        0: 'translation',
        1: 'all-translations',
        2: 'original-language',
        5: 'possible-translations',
        6: 'confidence',
        7: 'possible-mistakes',
        8: 'language',
        11: 'synonyms',
        12: 'definitions',
        13: 'examples',
        14: 'see-also',
    }

    @classmethod
    def _get_params(cls: type[Self], src_lang: str, dest_lang: str, text: str) -> dict:
        return {
            'client': 'gtx',
            'sl': src_lang,
            'tl': dest_lang,
            'hl': dest_lang,
            'dt': ['at', 'bd', 'ex', 'ld', 'md', 'qca', 'rw', 'rm', 'ss', 't'],
            'ie': 'UTF-8',
            'oe': 'UTF-8',
            'otf': 1,
            'ssel': 0,
            'tsel': 0,
            'tk': 'qwerty',
            'q': text,
        }

    @classmethod
    async def translate(
        cls: type[Self],
        text: str,
        src_lang: str,
        dest_lang: str,
    ) -> TranslationSchema:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                'https://translate.googleapis.com/translate_a/single',
                params=cls._get_params(src_lang=src_lang, dest_lang=dest_lang, text=text),
                headers={'User-Agent': cls.USER_AGENT},
            )
            r.raise_for_status()
            r_json = r.json()

        translated_text = ''.join([d[0] if d[0] else '' for d in r_json[0]])
        extra_data = {name: d for i, d in enumerate(r_json) if (name := cls.NAME_MAPPING.get(i))}

        return TranslationSchema.model_validate(
            {
                'dest': dest_lang,
                'extra_data': extra_data,
                'origin': text,
                'src': src_lang,
                'text': translated_text,
            },
        )
