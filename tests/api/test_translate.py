import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from pytest_httpx import HTTPXMock

from app.services.google_translate import GoogleTranslateService


@pytest.fixture(scope='session')
def path_() -> str:
    return '/v1/translate'


@pytest.fixture
def word(faker: Faker) -> str:
    return faker.word()


@pytest.fixture
def google_translate_response(word: str) -> list:
    return [
        [
            ['испытание', word, None, None, 10],
            [None, None, 'ispytaniye', 'ˈCHalənj'],  # noqa: RUF001
        ],
        [
            [
                'имя существительное',
                [
                    'вызов',
                    'проблема',
                ],
                [
                    [
                        'вызов',
                        ['call', word, 'invocation', 'summons', 'defiance', 'dare'],
                        None,
                        0.20316233,
                    ],
                    [
                        'проблема',
                        ['problem', 'issue', word, 'question', 'poser', 'proposition'],
                        None,
                        0.060054667,
                    ],
                ],
                word,
                1,
            ],
            [
                'глагол',
                [
                    'оспаривать',
                    'бросать вызов',
                ],
                [
                    [
                        'оспаривать',
                        [word, 'dispute', 'contest', 'contend', 'debate', 'litigate'],
                        None,
                        0.10539922,
                    ],
                    [
                        'бросать вызов',
                        [word, 'defy', 'affront', 'outdare', 'bid defiance to'],
                        None,
                        0.014717029,
                    ],
                ],
                word,
                2,
            ],
        ],
        'en',
        None,
        None,
        [
            [
                word,
                None,
                [
                    ['испытание', 1000, True, False, [10]],
                    ['бросать вызов', 1000, True, False, [10]],
                    ['вызов', 1000, True, False, [1, 3], None, [[3]]],
                ],
                [[0, 9]],
                word,
                0,
                0,
            ],
        ],
        0.83768755,
        [],
        [['en'], None, [0.83768755], ['en']],
        None,
        None,
        [
            [
                'имя существительное',
                [
                    [['dare', 'provocation', 'summons'], 'm_en_gbus0167500.006'],
                    [
                        [
                            'problem',
                            'difficult task',
                            'test',
                            'trial',
                            'trouble',
                            'bother',
                            'obstacle',
                        ],
                        'm_en_gbus0167500.009',
                    ],
                ],
                word,
                1,
            ],
            [
                'глагол',
                [
                    [
                        [
                            'test',
                            'tax',
                            'try',
                        ],
                        'm_en_gbus0167500.047',
                    ],
                ],
                word,
                2,
            ],
        ],
        [
            [
                'имя существительное',
                [
                    [
                        'a call to take part in a contest or competition, especially a duel.',
                        'm_en_gbus0167500.006',
                        'he accepted the challenge',
                    ],
                ],
                word,
                1,
            ],
            [
                'глагол',
                [
                    [
                        'invite (someone) to engage in a contest.',
                        'm_en_gbus0167500.038',
                        'he challenged one of my men to a duel',
                    ],
                ],
                word,
                2,
            ],
        ],
        [
            [
                [
                    'he needed something both to <b>challenge</b> his skills and to regain '
                    'his crown as the king of the thriller',
                    None,
                    None,
                    None,
                    None,
                    'm_en_gbus0167500.047',
                ],
                [
                    'a <b>challenge</b> to the legality of the order',
                    None,
                    None,
                    None,
                    None,
                    'm_en_gbus0167500.012',
                ],
            ],
        ],
    ]


@pytest.fixture
def mock_google_request(google_translate_response: list, httpx_mock: HTTPXMock) -> HTTPXMock:
    httpx_mock.add_response(
        status_code=status.HTTP_200_OK,
        json=google_translate_response,
        method='GET',
        match_headers={'User-Agent': GoogleTranslateService.USER_AGENT},
    )
    return httpx_mock


@pytest.mark.asyncio()
async def test_create_translation(
    client: AsyncClient,
    path_: str,
    word: str,
    faker: Faker,
    mock_google_request: HTTPXMock,
) -> None:
    # cache miss
    r = await client.post(path_, json={'text': word, 'src_lang': 'en', 'dest_lang': 'ru'})
    assert r.status_code == status.HTTP_200_OK, r.text
    assert r.json()
    assert len(mock_google_request.get_requests()) == 1

    # from cache
    r = await client.post(path_, json={'text': word, 'src_lang': 'en', 'dest_lang': 'ru'})
    assert r.status_code == status.HTTP_200_OK, r.text
    assert r.json()
    assert len(mock_google_request.get_requests()) == 1

    # incorrect input language
    r = await client.post(
        path_,
        json={'text': word, 'src_lang': 'en', 'dest_lang': faker.pystr()},
    )
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, r.text

    # same languages
    r = await client.post(path_, json={'text': word, 'src_lang': 'en', 'dest_lang': 'en'})
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, r.text


@pytest.mark.asyncio()
async def test_get_list_translation(
    client: AsyncClient,
    path_: str,
    word: str,
    faker: Faker,
    mock_google_request: HTTPXMock,  # noqa: ARG001
) -> None:
    # create
    r = await client.post(path_, json={'text': word, 'src_lang': 'en', 'dest_lang': 'ru'})
    assert r.status_code == status.HTTP_200_OK, r.text

    # existing word
    pattern = word[1:-1]
    r = await client.get(path_, params={'sort': ['-created_at'], 'searched_word': pattern})
    assert r.status_code == status.HTTP_200_OK, r.text
    assert (r_json := r.json()) and len(items := r_json['items']) == 1
    assert items[0]['text'] == word
    expected_keys = {
        'definitions',
        'dest_lang',
        'examples',
        'src_lang',
        'synonyms',
        'text',
        'translations',
    }
    assert set(items[0].keys()) == expected_keys

    r = await client.get(
        path_,
        params={
            'sort': ['-created_at'],
            'searched_word': pattern,
            'include_definition': True,
            'include_synonyms': True,
        },
    )
    assert r.status_code == status.HTTP_200_OK, r.text
    assert (r_json := r.json()) and len(items := r_json['items']) == 1
    assert set(items[0].keys()) == expected_keys | {'definitions', 'synonyms'}

    # not existing word
    r = await client.get(path_, params={'sort': ['-created_at'], 'searched_word': faker.pystr()})
    assert r.status_code == status.HTTP_200_OK, r.text
    assert (r_json := r.json()) and len(r_json['items']) == 0


@pytest.mark.asyncio()
async def test_remove_translation(
    client: AsyncClient,
    path_: str,
    word: str,
    faker: Faker,
    mock_google_request: HTTPXMock,  # noqa: ARG001
) -> None:
    # create
    r = await client.post(path_, json={'text': word, 'src_lang': 'en', 'dest_lang': 'ru'})
    assert r.status_code == status.HTTP_200_OK, r.text

    # remove existing item
    r = await client.delete(path_, params={'word': word})
    assert r.status_code == status.HTTP_204_NO_CONTENT, r.text

    # remove not existing item
    r = await client.delete(path_, params={'word': faker.pystr()})
    assert r.status_code == status.HTTP_204_NO_CONTENT, r.text
