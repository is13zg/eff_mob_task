# services/rbac_seed.py
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession



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

    await db.execute(text("""
            INSERT INTO roles (name)
            SELECT 'user'
            WHERE NOT EXISTS (SELECT 1 FROM roles WHERE name = 'user');
        """))
    await db.execute(text("""
            INSERT INTO user_roles (user_id, role_id)
            SELECT u.id, r.id
            FROM users u
            CROSS JOIN (SELECT id FROM roles WHERE name = 'user') r
            WHERE NOT EXISTS (
                SELECT 1 FROM user_roles ur WHERE ur.user_id = u.id AND ur.role_id = r.id
            );
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
