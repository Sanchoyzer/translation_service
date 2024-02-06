from typing import ClassVar

from mongodb_migrations.base import BaseMigration
from pymongo import ASCENDING, IndexModel


class Migration(BaseMigration):
    RUN_INDEXES: ClassVar[list] = [
        IndexModel([('text', ASCENDING)]),
        IndexModel([('src_lang', ASCENDING)]),
        IndexModel([('dest_lang', ASCENDING)]),
    ]

    def upgrade(self) -> None:
        collection = self.db.get_collection('translate')
        collection.create_indexes(self.RUN_INDEXES)

    def downgrade(self) -> None:
        collection = self.db.get_collection('translate')
        for idx in self.RUN_INDEXES:
            collection.drop_index(idx.document['name'])
