#!/bin/bash

output=${1:-~/.clang-format}

clang-format -style=llvm -dump-config >$output
sed -i 's/ColumnLimit:.*/ColumnLimit:     180/' $output
sed -i 's/^IndentWidth:.*/IndentWidth:     4/' $output
sed -i 's/AllowShortBlocksOnASingleLine:.*/AllowShortBlocksOnASingleLine: true/' $output
sed -i 's/AllowShortLoopsOnASingleLine:.*/AllowShortLoopsOnASingleLine: true/' $output
sed -i 's/BreakBeforeBraces:.*/BreakBeforeBraces: Linux/' $output
sed -i 's/AllowShortFunctionsOnASingleLine:.*/AllowShortFunctionsOnASingleLine: false/' $output
sed -i 's/AllowShortIfStatementsOnASingleLine:.*/AllowShortIfStatementsOnASingleLine: true/' $output
sed -i 's/SortIncludes:.*/SortIncludes:    false/' $output
