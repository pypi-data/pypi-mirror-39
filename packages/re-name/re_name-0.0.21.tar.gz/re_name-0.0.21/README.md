# Example Package

This is a tool that you can update file names in batch

### ![#1589F0](https://placehold.it/15/1589F0/000000?text=+) `re_name [old patten] [new patten]`

#### optional parameters

    -f --file This will make changes on file(s), you can only review the changes without this
    --ext        Specify the file types you want to update
    -s --suffix  Will append suffix. # stands for the sequence for file list

#### re_name -p '\-\d' ""
    hello1-1.txt  ---->  hello1.txt

#### re_name 55 ll -s "#"
    he55o1.txt  ---->  hello1-1.txt
    he55o2.txt  ---->  hello2-2.txt
    he55o3.txt  ---->  hello3-3.txt