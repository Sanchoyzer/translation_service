from enum import StrEnum, unique
from typing import Self

from pydantic import field_validator, model_validator

from app.schemas.base import RequestModel, ResponseAttrsModel, ResponseModel


@unique
class LanguageType(StrEnum):
    AF = 'af'
    SQ = 'sq'
    AM = 'am'
    AR = 'ar'
    HY = 'hy'
    AZ = 'az'
    EU = 'eu'
    BE = 'be'
    BN = 'bn'
    BS = 'bs'
    BG = 'bg'
    CA = 'ca'
    CEB = 'ceb'
    NY = 'ny'
    ZH_CN = 'zh-cn'
    ZH_TW = 'zh-tw'
    CO = 'co'
    HR = 'hr'
    CS = 'cs'
    DA = 'da'
    NL = 'nl'
    EN = 'en'
    EO = 'eo'
    ET = 'et'
    TL = 'tl'
    FI = 'fi'
    FR = 'fr'
    FY = 'fy'
    GL = 'gl'
    KA = 'ka'
    DE = 'de'
    EL = 'el'
    GU = 'gu'
    HT = 'ht'
    HA = 'ha'
    HAW = 'haw'
    IW = 'iw'
    HE = 'he'
    HI = 'hi'
    HMN = 'hmn'
    HU = 'hu'
    IS = 'is'
    IG = 'ig'
    ID = 'id'
    GA = 'ga'
    IT = 'it'
    JA = 'ja'
    JW = 'jw'
    KN = 'kn'
    KK = 'kk'
    KM = 'km'
    KO = 'ko'
    KU = 'ku'
    KY = 'ky'
    LO = 'lo'
    LA = 'la'
    LV = 'lv'
    LT = 'lt'
    LB = 'lb'
    MK = 'mk'
    MG = 'mg'
    MS = 'ms'
    ML = 'ml'
    MT = 'mt'
    MI = 'mi'
    MR = 'mr'
    MN = 'mn'
    MY = 'my'
    NE = 'ne'
    NO = 'no'
    OR = 'or'
    PS = 'ps'
    FA = 'fa'
    PL = 'pl'
    PT = 'pt'
    PA = 'pa'
    RO = 'ro'
    RU = 'ru'
    SM = 'sm'
    GD = 'gd'
    SR = 'sr'
    ST = 'st'
    SN = 'sn'
    SD = 'sd'
    SI = 'si'
    SK = 'sk'
    SL = 'sl'
    SO = 'so'
    ES = 'es'
    SU = 'su'
    SW = 'sw'
    SV = 'sv'
    TG = 'tg'
    TA = 'ta'
    TE = 'te'
    TH = 'th'
    TR = 'tr'
    UK = 'uk'
    UR = 'ur'
    UG = 'ug'
    UZ = 'uz'
    VI = 'vi'
    CY = 'cy'
    XH = 'xh'
    YI = 'yi'
    YO = 'yo'
    ZU = 'zu'


class TranslateRequest(RequestModel):
    text: str
    src_lang: LanguageType
    dest_lang: LanguageType

    @field_validator('text')
    @classmethod
    def get_only_one_word(cls: type[Self], v: str) -> str:
        return v.split(maxsplit=1)[0]

    @model_validator(mode='after')
    def check_languages(self) -> Self:
        if self.src_lang == self.dest_lang:
            raise ValueError('Source and destination languages are the same')
        return self


class TranslateResponse(ResponseAttrsModel):
    text: str
    src_lang: LanguageType
    dest_lang: LanguageType
    definitions: dict[str, list[str]]
    synonyms: dict[str, list[str]]
    translations: dict[str, list[str]]
    examples: list[str]


class WordResponse(ResponseModel):
    text: str
    src_lang: LanguageType
    dest_lang: LanguageType
    definitions: dict[str, list[str]] | None = None
    synonyms: dict[str, list[str]] | None = None
    translations: dict[str, list[str]] | None = None
    examples: list[str]


class WordsResponse(ResponseModel):
    items: list[WordResponse]
