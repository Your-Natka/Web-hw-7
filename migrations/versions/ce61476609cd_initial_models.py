"""Initial models

Revision ID: ce61476609cd
Revises: 
Create Date: 2025-07-29 18:25:34.914948
"""

from typing import Sequence, Union
from sqlalchemy.sql import text
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce61476609cd'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Додаємо колонку date_of
    op.add_column('grades', sa.Column('date_of', sa.Date(), nullable=True))
    op.alter_column('grades', 'grade',
                    existing_type=sa.INTEGER(),
                    nullable=False)
    op.drop_column('grades', 'grade_date')

    # Унікальні групи
    op.execute(text("""
        DELETE FROM groups
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM groups
            GROUP BY name
        );
    """))
    op.create_unique_constraint(None, 'groups', ['name'])

    # === STUDENTS ===
    op.add_column('students', sa.Column('fullname', sa.String(length=100), nullable=True))

    # Копіюємо дані з full_name до fullname
    op.execute(text("""
        UPDATE students SET fullname = full_name WHERE full_name IS NOT NULL;
    """))

    # Видаляємо записи з NULL
    op.execute(text("""
        DELETE FROM students WHERE fullname IS NULL;
    """))

    # Змінюємо колонку на NOT NULL
    op.alter_column('students', 'fullname', nullable=False)

    # Видаляємо стару колонку
    op.drop_column('students', 'full_name')

    # === TEACHERS ===
    op.add_column('teachers', sa.Column('fullname', sa.String(length=100), nullable=True))

    op.execute(text("""
        UPDATE teachers SET fullname = full_name WHERE full_name IS NOT NULL;
    """))

    op.execute(text("""
        DELETE FROM teachers WHERE fullname IS NULL;
    """))

    op.alter_column('teachers', 'fullname', nullable=False)

    op.drop_column('teachers', 'full_name')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('teachers', sa.Column('full_name', sa.VARCHAR(length=100), nullable=True))
    op.drop_column('teachers', 'fullname')

    op.add_column('students', sa.Column('full_name', sa.VARCHAR(length=100), nullable=False))
    op.drop_column('students', 'fullname')

    op.drop_constraint(None, 'groups', type_='unique')

    op.add_column('grades', sa.Column('grade_date', sa.DATE(), nullable=False))
    op.alter_column('grades', 'grade',
                    existing_type=sa.INTEGER(),
                    nullable=True)
    op.drop_column('grades', 'date_of')
