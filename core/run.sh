#!/bin/bash

EXPERIMENT_NUMBER="0.0.0"
CONTAINER="vinh-swift-experiemnts"
FILE_PATH="./experiment_data/file_1T.h5"
SEGMENT_SIZE="5G"
THREAD=()
FILE_SPLIT_SIZE=()

extract_result () {

}

save_result () {
    sqlite3 ./db/experiments_dev.db "INSERT INTO Experiment VALUES('cac.h5','0.0.0', 'bucket', 'mahti','login','swift','100G','5G',10,NULL,NULL,'200Mb/s','1h');"
}

## Run experiments wit swift:
for file in ./experiment_data/*
do
    for segment_size in "1G" "2G" "5G"
    do
        swift upload --use-slo --segment-size $segment_size $SWIFT $file
        # TODO: script to extract and save experiment's metadata
    done
done

#if [ -f ./db/experiments_dev.db ]
#then
#    rm ./db/experiments_dev.db
#fi
#sqlite3 ./db/experiments_dev.db < ./db/create_tables.sql
#sqlite3 ./db/experiments_dev.db "INSERT INTO File VALUES('cac.h5', '.h5', '1T');"
#sqlite3 ./db/experiments_dev.db "INSERT INTO Experiment VALUES('cac.h5','0.0.0', 'bucket', 'mahti','login','swift','100G','5G',10,NULL,NULL,'200Mb/s','1h');"
