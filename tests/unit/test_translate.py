import math
from collections.abc import Callable

import pytest
from faker import Faker

from app.models.translate import Translate
from app.repositories.translate import translation_repo
from app.schemas.translate import LanguageType


@pytest.fixture
def f_translations(faker: Faker) -> Callable[[], Translate]:
    def inner():
        return Translate.model_validate(
            {
                'text': faker.word(),
                'src_lang': faker.enum(LanguageType),
                'dest_lang': faker.enum(LanguageType),
                'definitions': {faker.pystr(): faker.pylist(allowed_types=[str])},
                'synonyms': {faker.pystr(): faker.pylist(allowed_types=[str])},
                'translations': {faker.pystr(): faker.pylist(allowed_types=[str])},
                'examples': faker.pylist(allowed_types=[str]),
            },
        )

    return inner


@pytest.mark.asyncio()
async def test_repo_create_and_delete(f_translations: Callable, faker: Faker) -> None:
    docs = await translation_repo.get_list(page=0, page_size=10)
    assert len(docs) == 0

    in_translation = f_translations()
    doc = await translation_repo.create_one(document=in_translation)
    assert doc and doc.id and doc.created_at

    docs = await translation_repo.get_list(page=0, page_size=10)
    assert len(docs) == 1 and docs[0].id == doc.id

    deleted_count = await translation_repo.delete(criteria={'text': faker.pystr()})
    assert deleted_count == 0

    deleted_count = await translation_repo.delete(criteria={'text': doc.text})
    assert deleted_count == 1
    docs = await translation_repo.get_list(page=0, page_size=10)
    assert len(docs) == 0


@pytest.mark.asyncio()
async def test_repo_filtration(f_translations: Callable, faker: Faker) -> None:
    docs = await translation_repo.get_list(page=0, page_size=100)
    assert len(docs) == 0

    translations = []
    for _ in range(faker.pyint(min_value=3, max_value=20)):
        in_translation = f_translations()
        doc = await translation_repo.create_one(document=in_translation)
        translations.append(doc)

    # test paging
    page_size = faker.pyint(min_value=2, max_value=5)
    total_items = 0
    for i in range(math.ceil(len(translations) / page_size)):
        docs = await translation_repo.get_list(page=i, page_size=page_size)
        total_items += len(docs)
    assert total_items == len(translations)

    # test sorting
    docs = await translation_repo.get_list(page=0, page_size=100, sort=['created_at'])
    reversed_docs = await translation_repo.get_list(page=0, page_size=100, sort=['-created_at'])
    assert docs == reversed_docs[::-1]

    # test filtering
    original_docs = docs.copy()

    docs = await translation_repo.get_list(page=0, page_size=100, searched_word=faker.pystr())
    assert len(docs) == 0

    doc_name = original_docs[0].text
    docs = await translation_repo.get_list(page=0, page_size=100, searched_word=doc_name)
    assert len(docs) == len([i for i in original_docs if doc_name in i.text])

    doc_name = original_docs[0].text[1:-1]
    docs = await translation_repo.get_list(page=0, page_size=100, searched_word=doc_name)
    assert len(docs) == len([i for i in original_docs if doc_name in i.text])

    doc_name = ''.join([i if faker.pybool() else i.upper() for i in doc_name])
    docs = await translation_repo.get_list(page=0, page_size=100, searched_word=doc_name)
    assert len(docs) == len([i for i in original_docs if doc_name.lower() in i.text.lower()])
