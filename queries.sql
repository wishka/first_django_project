select "django_session"."session_key", "django_session"."session_data", "django_session"."expire_date" from "django_session" where ("django_session"."expire_date" > '2023-12-20 19:09:20.012414' and "django_session"."session_key" = 'fexh9o4xuh4zuz3tlqegn49en1zskrjy') LIMIT 21; args=('2023-12-20 19:09:20.012414', 'fexh9o4xuh4zuz3tlqegn49en1zskrjy'); alias=default
select "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" from "auth_user" where "auth_user"."id" = 1 LIMIT 21; args=(1,); alias=default
select "myauth_profile"."id", "myauth_profile"."user_id", "myauth_profile"."bio", "myauth_profile"."agreement_accepted", "myauth_profile"."avatar" from "myauth_profile" where "myauth_profile"."user_id" = 1 LIMIT 21; args=(1,); alias=default
select "shopapp_product"."id", "shopapp_product"."name", "shopapp_product"."description", "shopapp_product"."price", "shopapp_product"."discount", "shopapp_product"."created_at", "shopapp_product"."archived", "shopapp_product"."created_by_id", "shopapp_product"."preview" from "shopapp_product" order by "shopapp_product"."name" asc, "shopapp_product"."price" asc;


select "shopapp_product"."id",
       "shopapp_product"."name",
        "shopapp_product"."description",
        "shopapp_product"."price",
        "shopapp_product"."discount",
        "shopapp_product"."created_at",
        "shopapp_product"."archived",
        "shopapp_product"."created_by_id",
        "shopapp_product"."preview"
from "shopapp_product" where "shopapp_product"."id" = 2 LIMIT 21;
select "shopapp_productimage"."id", "shopapp_productimage"."product_id", "shopapp_productimage"."image", "shopapp_productimage"."description" from "shopapp_productimage" where "shopapp_productimage"."product_id" in (2); args=(2,); alias=default
select "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" from "auth_user" where "auth_user"."id" = 1 LIMIT 21;
select "django_session"."session_key", "django_session"."session_data", "django_session"."expire_date" from "django_session" where ("django_session"."expire_date" > '2023-12-20 19:13:02.547277' and "django_session"."session_key" = 'fexh9o4xuh4zuz3tlqegn49en1zskrjy') LIMIT 21; args=('2023-12-20 19:13:02.547277', 'fexh9o4xuh4zuz3tlqegn49en1zskrjy');
select "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" from "auth_user" where "auth_user"."id" = 1 LIMIT 21;
select "myauth_profile"."id", "myauth_profile"."user_id", "myauth_profile"."bio", "myauth_profile"."agreement_accepted", "myauth_profile"."avatar" from "myauth_profile" where "myauth_profile"."user_id" = 1 LIMIT 21; args=(1,); alias=default


select "django_session"."session_key", "django_session"."session_data", "django_session"."expire_date" from "django_session" where ("django_session"."expire_date" > '2023-12-22 03:49:55.724692' and "django_session"."session_key" = 'fexh9o4xuh4zuz3tlqegn49en1zskrjy') LIMIT 21; args=('2023-12-22 03:49:55.724692', 'fexh9o4xuh4zuz3tlqegn49en1zskrjy'); alias=default
select "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" from "auth_user" where "auth_user"."id" = 1 LIMIT 21; args=(1,); alias=default
select "myauth_profile"."id", "myauth_profile"."user_id", "myauth_profile"."bio", "myauth_profile"."agreement_accepted", "myauth_profile"."avatar" from "myauth_profile" where "myauth_profile"."user_id" = 1 LIMIT 21; args=(1,); alias=default
select "blogapp_article"."id", "BlogApp_article"."title", "BlogApp_article"."content", "BlogApp_article"."pub_date", "BlogApp_article"."author_id", "BlogApp_article"."category_id" from "BlogApp_article"; args=(); alias=default


(0.001) SELECT "django_session"."session_key", "django_session"."session_data", "django_session"."expire_date" FROM "django_session" WHERE ("django_session"."expire_date" > '2023-12-22 03:57:19.460650' AND "django_session"."session_key" = 'fexh9o4xuh4zuz3tlqegn49en1zskrjy') LIMIT 21; args=('2023-12-22 03:57:19.460650', 'fexh9o4xuh4zuz3tlqegn49en1zskrjy'); alias=default
(0.000) SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."id" = 1 LIMIT 21; args=(1,); alias=default
(0.000) SELECT "myauth_profile"."id", "myauth_profile"."user_id", "myauth_profile"."bio", "myauth_profile"."agreement_accepted", "myauth_profile"."avatar" FROM "myauth_profile" WHERE "myauth_profile"."user_id" = 1 LIMIT 21; args=(1,); alias=default
(0.000) SELECT "BlogApp_article"."id", "BlogApp_article"."title", "BlogApp_article"."content", "BlogApp_article"."pub_date", "BlogApp_article"."author_id", "BlogApp_article"."category_id" FROM "BlogApp_article"; args=(); alias=default


(0.001) SELECT "django_session"."session_key", "django_session"."session_data", "django_session"."expire_date" FROM "django_session" WHERE ("django_session"."expire_date" > '2023-12-23 11:48:11.593490' AND "django_session"."session_key" = 'hd0hwjh0ti2be4ip3kyhr9ra7ury8af5') LIMIT 21; args=('2023-12-23 11:48:11.593490', 'hd0hwjh0ti2be4ip3kyhr9ra7ury8af5'); alias=default
(0.000) SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."id" = 6 LIMIT 21; args=(6,); alias=default
(0.000) SELECT "myauth_profile"."id", "myauth_profile"."user_id", "myauth_profile"."bio", "myauth_profile"."agreement_accepted", "myauth_profile"."avatar" FROM "myauth_profile" WHERE "myauth_profile"."user_id" = 6 LIMIT 21; args=(6,); alias=default
(0.000) SELECT "BlogApp_article"."id", "BlogApp_article"."title", "BlogApp_article"."content", "BlogApp_article"."pub_date", "BlogApp_article"."author_id", "BlogApp_article"."category_id", "BlogApp_author"."id", "BlogApp_author"."name", "BlogApp_author"."bio" FROM "BlogApp_article" INNER JOIN "BlogApp_author" ON ("BlogApp_article"."author_id" = "BlogApp_author"."id") ORDER BY "BlogApp_article"."pub_date" ASC; args=(); alias=default
(0.000) SELECT "django_content_type"."app_label", "auth_permission"."codename" FROM "auth_permission" INNER JOIN "auth_user_user_permissions" ON ("auth_permission"."id" = "auth_user_user_permissions"."permission_id") INNER JOIN "django_content_type" ON ("auth_permission"."content_type_id" = "django_content_type"."id") WHERE "auth_user_user_permissions"."user_id" = 6; args=(6,); alias=default
(0.001) SELECT "django_content_type"."app_label", "auth_permission"."codename" FROM "auth_permission" INNER JOIN "auth_group_permissions" ON ("auth_permission"."id" = "auth_group_permissions"."permission_id") INNER JOIN "auth_group" ON ("auth_group_permissions"."group_id" = "auth_group"."id") INNER JOIN "auth_user_groups" ON ("auth_group"."id" = "auth_user_groups"."group_id") INNER JOIN "django_content_type" ON ("auth_permission"."content_type_id" = "django_content_type"."id") WHERE "auth_user_groups"."user_id" = 6; args=(6,); alias=default


SELECT "django_session"."session_key", "django_session"."session_data", "django_session"."expire_date" FROM "django_session" WHERE ("django_session"."expire_date" > '2023-12-24 12:43:15.666254' AND "django_session"."session_key" = 'tqe6j1iop1unmvlb5o9209r7f9yksu8d') LIMIT 21; args=('2023-12-24 12:43:15.666254', 'tqe6j1iop1unmvlb5o9209r7f9yksu8d');
SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."id" = 1 LIMIT 21;
SELECT "BlogApp_category"."id", "BlogApp_category"."name" FROM "BlogApp_category" WHERE "BlogApp_category"."id" = 1 LIMIT 21;
SELECT "BlogApp_tag"."id", "BlogApp_tag"."name" FROM "BlogApp_tag" WHERE "BlogApp_tag"."id" IN (1);
SELECT 1 AS "a" FROM "BlogApp_category" WHERE "BlogApp_category"."id" = 1 LIMIT 1;
SELECT "BlogApp_author"."id", "BlogApp_author"."name", "BlogApp_author"."bio" FROM "BlogApp_author" WHERE "BlogApp_author"."name" = 'wishka' LIMIT 21; args=('wishka',);
Total exceptions: 2
SELECT "BlogApp_author"."id", "BlogApp_author"."name", "BlogApp_author"."bio" FROM "BlogApp_author" ORDER BY "BlogApp_author"."name" ASC LIMIT 21;
