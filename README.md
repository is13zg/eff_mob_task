<h2>Описание  схемы  структуры управления ограничениями доступа. </h2>

В БД созданы таблицы users, roles, role_element_access, resourse_elements
В таблице users хранится инфа о пользователе, она через промежуточную таблицу и ИД связана с roles. 
resourse_elements хранит все виды ресурсов, которые доступны в приложении.
Таблица role_element_access для каждой роли, каждого вида ресурсов и кажого действия (CRUD) хранит уровень дотсупа (all, own, none).
Т.е. при попытке получить доступ к ресурсу, определяется пользователь(ИД) и по этому определяются его роли(ИД), определяется вид ресурса(ИД),  выбранное действие (CRUD) и из БД вытаскиваем уровень дотсупа (all, own, none)


<h2>Для проверки работы можно использовать следующую БД:</h2>

DB_USER=pguser

DB_PASSWORD=pgpwd4user

DB_HOST=62.113.108.107

DB_PORT=5432

DB_NAME=main_db

SECRET_KEY=SECRET_KEY


<h3>Пользователи:</h3>
simple_user
{
  "email": "user2@example.com",
  "passwd": "string"
}


admin_user
{
  "email": "admin@example.com",
  "passwd": "adminadmin"
}
