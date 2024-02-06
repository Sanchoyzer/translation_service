from typing import Annotated

from fastapi import APIRouter, Query, status
from pydantic import NonNegativeInt, PositiveInt

from app.schemas.translate import TranslateRequest, TranslateResponse, WordsResponse
from app.services.translate import TranslateService


translate_router: APIRouter = APIRouter()


@translate_router.post('', response_model=TranslateResponse)
async def translate_word(data: TranslateRequest) -> TranslateResponse:
    result = await TranslateService.translate_word(data=data)
    return TranslateResponse.model_validate(result)


@translate_router.get('', response_model=WordsResponse)
async def get_list_words(  # noqa: PLR0913
    page: Annotated[NonNegativeInt, Query()] = 0,
    page_size: Annotated[PositiveInt, Query()] = 10,
    sort: Annotated[list[str] | None, Query()] = None,
    searched_word: Annotated[str | None, Query(min_length=1)] = None,
    *,
    include_definition: Annotated[bool, Query()] = False,
    include_synonyms: Annotated[bool, Query()] = False,
    include_translations: Annotated[bool, Query()] = False,
) -> WordsResponse:
    result = await TranslateService.get_list_words(
        page=page,
        page_size=page_size,
        sort=sort,
        searched_word=searched_word,
        include_definition=include_definition,
        include_synonyms=include_synonyms,
        include_translations=include_translations,
    )
    return WordsResponse.model_validate(result)


@translate_router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def remove_word(word: Annotated[str, Query(min_length=1)]) -> None:
    await TranslateService.remove_word(word=word)
