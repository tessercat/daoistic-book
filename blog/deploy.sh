#!/bin/bash
OUT=/opt/daoistic/blog/static/blog/img
ENTRIES=("ants-part-1" "ants-part-2" "setting-the-bar")
for entry in "${ENTRIES[@]}"; do
    echo cp $entry/header.jpg $OUT/$entry.jpg
    echo cp $entry/card.jpg $OUT/$entry-128.jpg
done
