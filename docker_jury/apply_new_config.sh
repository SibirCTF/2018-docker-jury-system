#!/bin/bash


echo "JURY_DB_HOST = $JURY_DB_HOST"
echo "JURY_DB_PORT = $JURY_DB_PORT"
echo "JURY_DB_NAME = $JURY_DB_NAME"
echo "JURY_DB_USER = $JURY_DB_USER"

nslookup $JURY_DB_HOST

# echo "JURY_DB_PASSWORD = $JURY_DB_PASSWORD"

sed -i -- 's/^dbhost.*$/dbhost = '$JURY_DB_HOST'/g' /usr/share/fhq-jury-ad/jury.d/conf.d/conf.ini
sed -i -- 's/^dbport.*$/dbport = '$JURY_DB_PORT'/g' /usr/share/fhq-jury-ad/jury.d/conf.d/conf.ini
sed -i -- 's/^dbname.*$/dbname = '$JURY_DB_NAME'/g' /usr/share/fhq-jury-ad/jury.d/conf.d/conf.ini
sed -i -- 's/^dbuser.*$/dbuser = '$JURY_DB_USER'/g' /usr/share/fhq-jury-ad/jury.d/conf.d/conf.ini
sed -i -- 's/^dbpass.*$/dbpass = '$JURY_DB_PASSWORD'/g' /usr/share/fhq-jury-ad/jury.d/conf.d/conf.ini