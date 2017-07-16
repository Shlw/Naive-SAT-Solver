#! /usr/bin/zsh

g++ make.cpp -o make
while true; do
./make>data.in
echo start
python3 cdcl.py data.in>ex.out
echo end
python3 main.py data.in>std.out
if diff ex.out std.out; then
    print AC
else
    echo WA
    exit 0
fi
done
