# services/rbac_seed.py
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

ACTIONS = ("create", "read", "update", "delete")

async def seed_rbac_minimal(db: AsyncSession) -> None:
    await db.execute(text("""
        INSERT INTO roles ( name) VALUES
          ('admin'), ('user')
        ON CONFLICT (name) DO NOTHING;
    """))
    await db.execute(text("""
        INSERT INTO recourse_elements (name)
        VALUES ('products')
        ON CONFLICT (name) DO NOTHING;
    """))

    # admin -> all
    await db.execute(text("""
            INSERT INTO role_element_access (role_id, element_id, action, level)
            SELECT r.id, e.id, acts.a, 'all'::levelenum
            FROM roles r
            JOIN recourse_elements e ON e.name = 'products'
            CROSS JOIN (
            VALUES 
            ('create'::actionenum),
            ('read'::actionenum),
            ('update'::actionenum),
            ('delete'::actionenum)
            ) AS acts(a)
            WHERE r.name = 'admin'
            ON CONFLICT (role_id, element_id, action)
            DO UPDATE SET level = EXCLUDED.level;

    """))

    # user -> own
    await db.execute(text("""
            INSERT INTO role_element_access (role_id, element_id, action, level)
            SELECT r.id, e.id, acts.a, 'own'::levelenum
            FROM roles r
            JOIN recourse_elements e ON e.name = 'products'
            CROSS JOIN (
            VALUES 
            ('create'::actionenum),
            ('read'::actionenum),
            ('update'::actionenum),
            ('delete'::actionenum)
            ) AS acts(a)
            WHERE r.name = 'user'
            ON CONFLICT (role_id, element_id, action)
            DO UPDATE SET level = EXCLUDED.level;

    """))
    await db.commit()
