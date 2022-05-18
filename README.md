# Magic API

## Create migration

To add or alter a database table you must use the alembic library, as SQLAlchemy recommends.

### Setting alembic

- In the first instance we must set the alembic.ini file at the root folder as the alembic.example.ini
- Alter the sqlalchemy.url variable as the example
- Create a new migration using the following
```sh
alembic revision -m "create user table"
```
- At ./database/migrations/versions we'll see a new created file, this file contains the requirments to make a migration, as the bellow
```python
"""create user table

Revision ID: d36f91b5f863
Revises: 
Create Date: 2022-05-18 18:39:35.494974

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd36f91b5f863'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """ 
        username: str
        first_name: str
        last_name: str
        password: str
        created_at: datetime
        updated_at: datetime

    """
    op.create_table('users',
        pass
    )


def downgrade():
    pass
```
there are some of the methods used to create or drop a specific table or column.
<table>
<thead>
  <tr>
    <th>Method</th>
    <th>Attribute</th>
    <th>Reverse</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>os.create_table('table_name',...)</td>
    <td>Create a new table with the sa.Column() columns</td>
    <td>os.drop_table('table_name')</td>
  </tr>
  <tr>
    <td>os.add_column('table_name', ...)</td>
    <td>Create new column on the given table</td>
    <td>os.drop_column('table_name','column_name')</td>
  </tr>
</tbody>
</table>
