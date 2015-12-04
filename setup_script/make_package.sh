#!/bin/bash
if [ -d package ];
  then
  rm -R package
fi
if [ -e package.tar.gz ];
  then
  rm package.tar.gz
fi
tar --exclude='make_package.sh' -zcvf package.tar.gz *
mkdir -p package
cd package
tar -zxvf ../package.tar.gz
cd ..
rm package.tar.gz
tar -zcvf package.tar.gz package
rm -R package
